# Google CTF 2016 : For2

**Category:** Forensics
**Points:** 200
**Solves:** 203
**Description:**
> Find the flag.

**Attached:** [capture.pcapng](https://github.com/b0tchsec/CTF-Fanny-Pack/blob/master/solutions/google_2016/For2/capture.pcapng)

## Write-up
### Investigate
Upon opening the caputre file with Wireshark, it's immediatly obvious that it contains USB traffic.  However, it wasn't obvious to me what device(s) the traffic is for.  I sorted the logs by 'Protocol' hoping for a protocol at a layer above USB.  Sure enough, there is one USBHID message.

My initial assumption was that this was keyboard traffic.  But intuitively, the data didn't appear to contain keypresses.  So after a few moments of looking at the logs, I remembered reading a writeup a few months ago for a CTF in which they were given a capture file containing USB traffic.

Sure enough, I found the writeup!  The folks at wiremask have written a great [writeup](https://wiremask.eu/writeups/boston-key-party-2015-riverside/) that helped me a tremendous amount in solving this challenge.

Using this filter:
```
usb.bDescriptorType
```

I was able to find the USB vendor and product ID:
```
idVendor: Logitech, Inc. (0x046d)
idProduct: M90/M100 Optical Mouse (0xc05a)
```

Yup, looks like a mouse to me!!  So I continue following right along with the other writeup.

### Code
I extracted the mouse data from the pcap-ng file using tshark.
```
$ tshark -r ./capture.pcapng -T fields -e usb.capdata > mouse_traffic.txt
```

Next, I wrote some code to read the mouse data from text into memory.
```python
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
```

And finally, plot the mouse traffic onto an image.
```python
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
```

### Output
![alt text](https://raw.githubusercontent.com/b0tchsec/CTF-Fanny-Pack/master/solutions/google_2016/For2/mouse_traffic.png "mouse_traffic.png")

After a little bruteforce to get the capitalization right, I finally get the scoreboard to accept the flag.
```
Flag: CTF{tHE_cAT_iS_the_cULpRiT}
```
