#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from PIL import Image
from numpy import asarray


def help():
    config = {
        'type': {'picture': ['.bmp', '.png']},
        'name': 'Emd'
    }
    return config


def reader(file):
    img = []
    for x in asarray(Image.open(file)):
        img += list(x)
    return img


def filter(data, bloc=70):
    charset = (32, 126)
    dec = bytes([x if charset[0] <= x <= charset[1] else ord('.') for x in data]).decode()
    return '\n'.join([
        '%s-%s | %s' % (i, (i + bloc), dec[i:(i + bloc)])
        for i in range(0, len(dec), bloc)
    ])


def decoder(pix, n, k):
    base = 2 * n + 1
    dec = []
    for i in range(0, len(pix), n * k):
        dec.append(int(''.join([
            str((pix[i + j * n] + 2 * pix[i + j * n + 1]) % base)
            for j in range(k)
        ]), base))
    return bytes(dec)


def scan(config):
    config_current = help()

    try:
        pix = reader(config['path'])
        data = decoder(pix, n=2, k=3)
        return {"type": "file", "path": "", "content": filter(data)}
    except:
        return {"type": "file", "path": "", "content": ""}

