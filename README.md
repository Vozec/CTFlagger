# CTFileScan-WEB
This website is used to scan automatically files during CTF. *(Mainly used for steganography)*


## Setup : 

```bash
docker build -t ctfweb .
docker run --rm -it -p 8080:80 ctfweb
```
The Website is available on your local machine on port *8080*

## Home :
![Alt Text](./img/home.png)
![Alt Text](./img/wait.png)

## Result:
![Alt Text](./img/result.png)

## Api Endpoint to retrieve results : 
```bash
Invoke-WebRequest -Uri https://localhost:8080/52062f33b7a58050c082a5f677a1ae626da32d88 -Method Get -Headers @{Api="True"} -UseBasicParsing  | Select-Object -Expand Content | .\jq.exe
```
![Alt Text](./img/json.png)


## Features :

## All:
  - Binwalk
  - Strings

### Images:
  - Color Palette swapper
  - Steghide extract
  - StegSeek 
  - Stegoveritas
  - LsbFilter
  - OpenStego
  - Outguess
  - Pngcheck
  - LSB Palette swap
  - Stegpy
  - Stegopvd
  - StegoPit
  - Stegolsb Bruteforce
  - Exiftool
  - Zsteg
  - Jsteg
  - StegExpose *(Lsb)*
  - Stegdetect
  - LsbSteg
  - LsbGraph
  - OpenStego
  - Outguess
  - Pngcheck
  - Gif Frame Extractor


### Audio:
  - Dmtf
  - HideMe
  - .Mid steg
  - Spectrogram
  
### Document:
  - Olevba
  - Pdfcrack
  - Pdfparser
  - Stegsnow

### ELF:
  - Strace
  - Ltrace
  - Steg86
  - Radare2

### Other:
  - .Pem/.Pub decoder *(Openssl)*
  - KcPassword decoder
  - Keepass *(Hash+Bruteforce)*
  - KeyChain Bruteforcer *(chainbreaker)*
  - RubberDucky bin decoder
  - ZipInfo / ZipDetails / Hash Zip + Bruteforce zip password

### Network:
  - Tshark *(HttpRequests)* + DNS
  - Pcapkit report
  - Ssldump
  - Rdpcap data & unhexlified data / UDP data
  - Urlsnarf
 
# Usage Of SSL Certificat :
You only have to edit this boolean in ``app.py``
```python
if __name__ == '__main__':
    debug = False
    ssl   = False
```

*Feel free to contribute to the project by adding different modules or suggesting future improvements*
