#!/usr/bin/env python

from socket import *
import sys,os
import struct
import pickle


#HOST='192.168.56.102'
HOST='127.0.0.1'
#HOST='172.16.60.254'
#HOST='172.16.30.32'
PORT=12777
BUFSIZ=10240
ADDR=(HOST,PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)

"""
login=False
logout = False
while login != True:
	ret = raw_input().strip()
	tcpCliSock.send('%s\r\n' % ret)
	data = tcpCliSock.recv(BUFSIZ)
	print data
	if "login_sucess" in data:
		login = True
		break

while True:
	data = raw_input(">")
	tcpCliSock.send('%s\r\n' % data)
	data = tcpCliSock.recv(BUFSIZ)
	if not data:
		break
	print data.strip()+"\n"
	if "seeyou" in data.strip():
		sys.exit(1)
"""

def close_socket():
	#tcpCliSock.shutdown(SHUT_RDWR)
	tcpCliSock.close()
	sys.exit(1)

data = ""
cmd = ""
try:
	data = sys.argv[1:]
except IndexError:
	data = 'help'
try:
	for cmds in data:
		cmd = cmds
except:
	sys.exit(1)


if "putfile" in cmd:
	filename = cmd.split(' ')[1]
	if not os.path.exists(filename):
		print "File not found!"
		close_socket()
	cmd = struct.pack('!1024s',cmd)
	tcpCliSock.send(cmd)
	try:
		fd = open(filename,'rb')
	except IOError,e:
		print "Something wrong happed! %s" % e
		close_socket()
	buf = ""
	while True:
		data = fd.read(1024)
		if not data:
			break
		data = data.encode('hex')
		tcpCliSock.send(data)
	fd.close()
	close_socket()

BUF_SIZE1 = struct.calcsize('!128s')
if "getfile" in cmd:
	filename = cmd.split(' ')[1].split('/')[-1]
	try:
		fp = open(filename,'wb')
	except IOError,e:
		print "errors happend while open %s! %s" % (filename,e)
		fp.close()
		close_socket()
	cmd = struct.pack('!0124s',cmd)
	tcpCliSock.send(cmd)
	rev = tcpCliSock.recv(BUF_SIZE1)
	ret = struct.unpack('!128s',rev)[0].replace('\x00','')
	if "not" in ret:
		print ret
		close_socket()
	else:
		while True:
			data = tcpCliSock.recv(1024)
			if not data:
				break
			fp.write(data.decode('hex'))
	fd.flush()
	fp.close()
	close_socket()

BUF_SIZE = struct.calcsize('!1024s')
cmd = struct.pack('!1024s',cmd)
tcpCliSock.send(cmd)
try:
	data = tcpCliSock.recv(BUF_SIZE)
	if not data or len(data)<=0:
		print "No data received!"
	print data.strip()+"\n"
finally:
	close_socket()

