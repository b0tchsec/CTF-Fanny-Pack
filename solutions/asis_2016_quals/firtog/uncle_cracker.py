#!/usr/bin/env python


def build_decoder_ring():
	decoder_ring = {}
	for c in range(32,126):
		code = hex(pow(c, 65537, 143))[2:]
		decoder_ring[code] = chr(c)
	return decoder_ring


def find_possible_matches(decoder_ring, two_char):
	return decoder_ring[two_char]


def crack_encoded_msg(encmsg):
	decoder_ring = build_decoder_ring()

	flag = ''
	i = 0
	while (i < len(encmsg)):
		try:
			flag += find_possible_matches(decoder_ring, encmsg[i] + encmsg[i+1])
			i += 2
		except:
			flag += find_possible_matches(decoder_ring, encmsg[i])
			i += 1
	return flag


def main():
	encflag = open('flag.txt', 'rb').read()
	flag = crack_encoded_msg(encflag)
	print(flag)


if __name__ == "__main__":
	main()
