#!/usr/bin/env python

import requests

URL = 'http://hack.bckdr.in/LOCATION-51/index.html'

#######################################################
# A normal web browser would download index.html,
# and then get redirected to trap.html.  From
# trap.html you can only view the fake flag.
# Instead, I download index.html, without redirecting,
# and it contains the base64-encoded flag.
#######################################################

def main():
	r = requests.get(URL)
	if r.status_code != 200:
		print('Failed: %d' % r.status_code)
		return

	# print the text
	print('HTML:\n%s' % r.text)


if __name__ == "__main__":
	main()
