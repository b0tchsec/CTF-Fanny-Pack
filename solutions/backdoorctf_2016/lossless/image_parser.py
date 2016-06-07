#!/usr/bin/env python
from PIL import Image

def img_diff_printer(img_orig, img_enc):
    X,Y = img_orig.size
    for x in range(X):
        for y in range(Y):
            pxl_orig = img_orig.getpixel((x,y))
            pxl_enc = img_enc.getpixel((x,y))
            if pxl_orig != pxl_enc:
                print('[%d, %d] %s != %s' % (x, y, str(pxl_orig), str(pxl_enc)))


def lsb_destego(img_orig, img_enc):
    decode = ''
    for x in range(50):
        byte = ''
        for y in range(7):
            pxl_orig = img_orig.getpixel((x,y))
            pxl_enc = img_enc.getpixel((x,y))
            if pxl_orig != pxl_enc:
                byte += '1'
            else:
                byte += '0'
        decode += chr(int(byte, 2))
    return decode


def main():
    img_orig = Image.open('original.png')
    img_enc = Image.open('encrypted.png')

    img_diff_printer(img_orig, img_enc)

    decode = lsb_destego(img_orig, img_enc)
    print(decode)


main()
