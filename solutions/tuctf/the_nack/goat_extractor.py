# read file contents into memory
f = open('ce6e1a612a1da91648306ace0cf7151e6531abc9.pcapng', 'rb')
content = f.read()
f.close()

#split on 'GOAT' + x01 byte (skipping the front part of file before GOAT starts)
goats = content.split('GOAT\x01')[1:]

#write the TCP data to a new file
f = open('goats.data', 'wb')
for i in goats:
	#data is in first 4 bytes, 5th byte should be null
	assert(i[4] == '\x00')
	data = i[:4]
	f.write(data)

f.close()

print('Goat data extracted...')
