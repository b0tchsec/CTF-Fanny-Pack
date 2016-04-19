HIDDEN_FILE_POSITON = 0x58FD00
hiddenfilename = 'hiddenfile.tiff'

f = open('rain.wav', 'rb')
content = f.read()
f.close()

f = open(hiddenfilename, 'wb')
f.write(content[HIDDEN_FILE_POSITON:])
f.close()
