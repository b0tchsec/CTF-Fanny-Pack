import base64
import sys

def main():
	if len(sys.argv) != 3:
		usage()
		return
	infile = sys.argv[1]
	outfile = sys.argv[2]
	print('Input file:  %s\nOutput file: %s' % (infile, outfile))
	b64_decode(infile, outfile)


def b64_decode(in_file, out_file):
	#Read the contents of the base64 encoded file, ignore newlines
	f = open(in_file, 'r')
	base64str = ''
	for line in f:
		base64str += line
	f.close()

	#Decode
	decoded = base64.b64decode(base64str)

	#write to a new file
	out = open(out_file, 'w')
	out.write(decoded)
	out.close()
	print('Wrote %d bytes to file: %s' % (len(decoded), out_file))


def usage():
	print('Usage:')
	print('./%s [INPUT - BASE64 Encoded] [OUTPUT - Decoded]' % sys.argv[0])


if __name__ == "__main__":
	main()
