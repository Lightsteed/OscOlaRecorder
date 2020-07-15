#!/usr/bin/python

from OSC import OSCServer,OSCClient, OSCMessage, ThreadingOSCServer
import sys
from time import sleep
import time
import types
import os
import subprocess
import threading
from threading import Thread
from os import listdir
from os.path import isfile, join
from random import shuffle
from random import sample

os.chdir('/home/pi/myoscrecs')
time.sleep(5)
server = ThreadingOSCServer( ("10.1.1.143", 7002) )# the ip adress of your pi/device goes here and the incoming OSC port you would like to use, i used 7002 for the port - the incoming port should be matched on your TouchOSC / OSC app

client = OSCClient()

#def handle_timeout(self):
#	print ("I'm IDLE")
#This here is just to do something while the script recieves no information....
#server.handle_timeout = types.MethodType(handle_timeout, server)

r = None
p = None
sr = 0
sp = 0
loop = 1
loopd = 10
shuffleloop = 1

def record(path, tags, args, source):
		split = path.split("/1/toggle")
		x = split.pop()
		state=int(args[0])
		print "Record",x
		global sr
		global r
		global sp
		global p
		if state == 1:
		  if sr == 0:
		 	 if sp == 0:
				r = subprocess.Popen(['ola_recorder', '-r', x, '-u 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20'], stdout=subprocess.PIPE)
			 	sr = 1
		   	 else:
				p.kill()
				r = subprocess.Popen(['ola_recorder', '-r', x, '-u 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20'], stdout=subprocess.PIPE)
                                sr = 1
				sp = 0
		  else:
		         if sp == 0:
				r.kill()
                         	r = subprocess.Popen(['ola_recorder', '-r', x, '-u 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20'], stdout=subprocess.PIPE)
			 	sr = 1
			 else:
				p.kill()
                                r = subprocess.Popen(['ola_recorder', '-r', x, '-u 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20'], stdout=subprocess.PIPE)
                                sr = 1
				sp = 0

		else:
			if sr == 0:
				None
			else: 
				r.kill()
				sr = 0

def playback(path, tags, args, source):
        split = path.split("/2/push")
        y = split.pop()
	state=int(args[0])
        print "Playback:",y
        global sp
	global p
	global sr
	global r
	if state == 1:
               		if sp == 0:
				if sr == 0:
					p = subprocess.Popen(['ola_recorder', '-p', y, '-i 0'], stdout=subprocess.PIPE)
					sp = 1
				else:
					r.kill()
					p = subprocess.Popen(['ola_recorder', '-p', y, '-i 0'], stdout=subprocess.PIPE)
                                        sp = 1
					sr = 0
			else:
				if sr == 0:
					p.kill()
					p = subprocess.Popen(['ola_recorder', '-p', y, '-i 0'], stdout=subprocess.PIPE)
					sp = 1
				else:
					p.kill()
					r.kill()
					p = subprocess.Popen(['ola_recorder', '-p', y, '-i 0'], stdout=subprocess.PIPE)
                                        sp = 1
					sr = 0

def stopallplay(path, tags, args, source):
		state=int(args[0])
		print "Stop All Playback:", state;
		global sp
		global p
        	if state == 1:
			p.kill()
			sp = 0

def stopallrec(path, tags, args, source):
        state=int(args[0])
        print "Stop All Recording:", state;
        global sr
        global r
        if state == 1:
                r.kill()
                sr = 0

def loopduration(path, tags, args, source):
		global loopd
		loopd=int(args[0])
#		print "Loop Duration", loopd;


def playall(path, tags, args, source):
		global loop
		state = int(args[0])
		loop=state
		if loop == 1:
			playallloop()

def shuffler(path, tags, args, source):
                global shuffleloop
                state = int(args[0])
                shuffleloop=state
                #if shuffle == 1:

def playallloop():
		global sp
		global p
		global sr
		global r
		global loop
		global loopd
		global shuffleloop
		while loop == 1:
		  if loop == 0:
			p.kill()
			break
		  print "Play on Loop";
		  file_list = os.listdir(r"/home/pi/myoscrecs")
		  #file_list_sorted = sorted([file_list, key=int)
	          file_shuffle = sample(file_list, len(file_list))
		  if shuffleloop == 0:
		   	files = sorted(file_list)
		  else:
			files = file_shuffle
		  for i in files:
		     if loop == 0:
			p.kill()
			break
	             #i = ""
		     #i = str(x)
		     print "Loop Duration", loopd;
		     if sp == 0:
                        if sr == 0:
                            	p = subprocess.Popen(['ola_recorder', '-p', i, '-i 0'], stdout=subprocess.PIPE)
                            	sp = 1
			else:
				r.kill()
				p = subprocess.Popen(['ola_recorder', '-p', i, '-i 0'], stdout=subprocess.PIPE)
				sp = 1
				sr = 0
                     else:
			if sr == 0:
				p.kill()
				p = subprocess.Popen(['ola_recorder', '-p', i, '-i 0'], stdout=subprocess.PIPE)
				sp = 1
			else:
				p.kill()
				r.kill()
				p = subprocess.Popen(['ola_recorder', '-p', i, '-i 0'], stdout=subprocess.PIPE)
				sp = 1
				sr = 0
			time.sleep(loopd)

#you can increase the amount of record and playback banks by increasing the number from 70 to whatever in the below lines.
for x in range(1,70):
	        server.addMsgHandler("/1/"+"toggle"+`x`, record)

for y in range(1,70):
                server.addMsgHandler("/2/"+"push"+`y`, playback)

server.addMsgHandler("/3/stopallplay", stopallplay)
server.addMsgHandler("/3/stopallrec", stopallrec)
server.addMsgHandler("/3/playall", playall)
server.addMsgHandler("/3/loopduration", loopduration)
server.addMsgHandler("/3/shuffle", shuffler)


#The way that the MSG Handlers work is by taking the values from set accessory, then it puts them into a function
#The function then takes the values and separates them according to their class (args, source, path, and tags)

while True:
	server.handle_request()

server.close()
#This will kill the server when the program ends


