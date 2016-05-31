cipher = '241 231 224 241 227 248 173 235 176 220 223 246 241 176 220 174 240 220 235 173 241 220 176 235 173 242 228 229 250 135'
key = 125

def main():
	plain = ''
	for val in cipher.split(' '):
		plain += chr(int(val)-key)
	print(plain)

main()

#tjctf{0n3_byt3_1s_n0t_3n0ugh}

