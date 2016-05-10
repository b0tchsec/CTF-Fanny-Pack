#!/usr/bin/env python
# Python template for pwning websites

import requests

URL = 'http://google.com/'

def main():
	# perform GET
	r = requests.get(URL)
	if r.status_code != requests.codes.OK:
		print('Failed: %d' % r.status_code)
		return

	# print the text and cookies
	print('HTML:\n%s' % r.text)
	print('Cookies:\n%s' % r.cookies)

	# create a new cookie
	spoofed_cookie = dict(username='admin')

	# perform GET with new cookie
	r = requests.get(URL, cookies=spoofed_cookie)
	if r.status_code != requests.codes.OK:
		print('Failed: %d' % r.status_code)
		return

	# perform POST
	r = requests.post(URL, data={'answer': '42'})
	if r.status_code != requests.codes.OK:
		print('Failed: %d' % r.status_code)
		return


if __name__ == "__main__":
	main()
