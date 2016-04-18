#!/usr/bin/env python

import requests

URL = 'http://hack.bckdr.in/LOST/'

def main():
	r = requests.get(URL)
	if r.status_code != 200:
		print('Failed: %d' % r.status_code)
		return

	# print the text
	print('HTML:\n%s' % r.text)

	#post on flag.php
	r = requests.post(URL+'flag.php')

	# print the text
	print('HTML:\n%s' % r.text)


if __name__ == "__main__":
	main()
