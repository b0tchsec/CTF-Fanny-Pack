#!/usr/bin/env python
import requests
import re
import json

URL = 'http://hack.bckdr.in/2013-MISC-75/misc75.php'

def isPrime(n):
	# see http://tinyurl.com/3dbhjv
	return re.match(r'^1?$|^(11+?)\1+$', '1' * n) == None


def getfirstPrimeNumbs(n):
	primes = []
	i = 0
	while len(primes) < n:
		if isPrime(i):
			primes.append(i)
		i += 1
	print('Prime calculation complete, length=%d' % n)
	return primes


def getSumOfFirstN(numbs, n):
	total = 0
	for i in range(n):
		total += numbs[i]
	return total



def main():
	#cache a bunch of primes
	primes = getfirstPrimeNumbs(1000)

	#Load the page
	r = requests.get(URL)
	if r.status_code != 200:
		print('Failed: %d' % r.status_code)
		return

	# print the text
	print('HTML:\n%s' % r.text)

	# print the cookies
	cookie = r.cookies
	print('Cookies:\n%s' % cookie)

	# read the page for the number of primes
	fIdx = r.text.index('First ') + len('First ')
	numb = r.text[fIdx:].split(' ')[0]
	print('My magic numb: %s' % numb)

	# calculate sum
	totalSum = getSumOfFirstN(primes, int(numb))

	#submit answer
	ans = {'Submit': 'Submit'}
	r = requests.post(URL, data={'answer':'%d' % totalSum}, cookies=cookie)
	if r.status_code != 200:
		print('Failed: %d' % r.status_code)
		return

	# print the text
	print('HTML:\n%s' % r.text)

	# print the cookies
	cookie = r.cookies
	print('Cookies:\n%s' % cookie)


if __name__ == "__main__":
	main()
