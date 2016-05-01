#!/usr/bin/env python

##################################################################
# Most code was borrowed from the following location:
# https://wiremask.eu/writeups/boston-key-party-2015-riverside/
##################################################################
import struct
import Image


TRAFFIC_FILE = 'mouse_traffic.txt'
INIT_X, INIT_Y = 1200, 500


#tshark -r ./capture.pcapng -T fields -e usb.capdata > mouse_traffic.txt
def parse_traffic_file(traffic_file):
    f = open(traffic_file, 'r')
    lines = f.readlines()
    f.close()
    good_lines = lines[97:]

    mouse_data = []

    for lin in good_lines:
        hex_bytes = lin.strip().split(':')
        b_bytes = ''
        for hx in hex_bytes:
            b = hx.decode('hex')
            b_bytes += b

        data = struct.unpack("bbbb", b_bytes)
        mouse_data.append(data)

    return mouse_data


#cursor movement in red, mouse clicks are black squares
def plot_mouse_traffic(mouse_data):
    picture = Image.new("RGB", (1600, 800), "white")
    pixels = picture.load()

    click_size = 4
    x, y = INIT_X, INIT_Y

    for data_point in mouse_data:
        status = data_point[0]
        x = x + data_point[1]
        y = y + data_point[2]

        if (status == 1):
            for i in range(-1*click_size, click_size):
                for j in range(-1*click_size, click_size):
                    pixels[x + i , y + j] = (0, 0, 0, 0)
        else:
            pixels[x, y] = (255, 0, 0, 0)

    print('Saving picture...')
    picture.save("mouse_traffic.png", "PNG")



def main():
    mouse_data = parse_traffic_file(TRAFFIC_FILE)
    plot_mouse_traffic(mouse_data)


if __name__ == "__main__":
    main()
