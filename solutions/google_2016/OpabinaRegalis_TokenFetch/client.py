#!/usr/bin/env python

import socket
import ssl
import main_pb2
import struct

TCP_IP = 'ssl-added-and-removed-here.ctfcompetition.com'
TCP_PORT = 1876


def pack_msg(msg):
	p = struct.pack('<I', len(msg)) + msg
	return p


def tx_msg(sock, msg):
	p = pack_msg(msg.SerializeToString())
	sock.send(p)


def print_req(req):
	print('VerbType: ' + repr(req.ver))
	print('URI: ' + repr(req.uri))
	print('Headers:')
	for i in req.headers:
		print(repr(i))
	print('Body: ' + repr(req.body))


def print_reply(rep):
	print('Status: ' + repr(rep.status))
	print('Headers:')
	for i in rep.headers:
		print(repr(i))
	print('Body: ' + repr(rep.body))


def print_ex(ex):
	if ex.HasField("request"):
		print_req(ex.request)
	if ex.HasField("reply"):
		print_reply(ex.reply)


def rx_msg(sock):
	data = sock.recv(4)
	if len(data) == 0:
		raise Exception('No data...')

	#Unpack the message length
	msg_len = struct.unpack('<I', data)[0]
	data = sock.recv(msg_len)

	#Read the protocol buffer message
	main_msg = main_pb2.Exchange()
	main_msg.ParseFromString(data)
	return main_msg


def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))

	# WRAP SOCKET
	ws = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23)

	#Get request
	data = rx_msg(ws)
	print_ex(data)

	#Reply
	new_dat = main_pb2.Exchange()
	new_dat.request.ver = main_pb2.Exchange.GET
	new_dat.request.uri = u'/token'
	new_dat.request.body = ''
	tx_msg(ws, new_dat)

	#Get the flag
	data = rx_msg(ws)
	print_ex(data)

	#Close the socket
	ws.close()


main()
