#!/usr/bin/python
import socket

ip = "192.168.1.81"
port = 31337

buffer = ["A"]
counter = 100
while len(buffer) <= 30:
	buffer.append("A" * counter)
	counter = counter + 100

for string in buffer:
	print "Fuzzing with %s bytes" % len(string)
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connect=s.connect((ip, port))
	s.send(string + '\r\n')
	data = s.recv(1024)
	s.close()
