import sys
import socket
import string
import urllib2
import json
import threading
import time
import random
import select
import re
import quotelib
import os
import linecache
import inspect
import commands
from datetime import datetime, timedelta, date
from secrets import PASS

RAW_CHATTERS = 'http://tmi.twitch.tv/group/user/%s/chatters'
CHANNEL_API = 'https://api.twitch.tv/kraken/channels/'
servers = [ {'PING': [0], 'readbuffer': "", 'HOST':"irc.twitch.tv",'PORT':6667,"channelfile":"channels.txt","socket":socket.socket(),'RUN':[0],'is_alive':[0]} ]
#{'PING': [0], 'readbuffer': "", 'HOST':"199.9.253.119",'PORT':443,"channelfile":"groups.txt","socket":socket.socket(),'RUN':[0],'is_alive':[0]}
OWNER="Abahbob"
NICK="Abahbot"
BOTMODS=["abahbob" , "thefuncannon"]
userlists={}
listcount=0
spamlimit=[0]
chan_rights = ""
bot_rights = ""
threshold = 60
t = ""
stream_info={}
FAQs = ""
quotes = quotelib.quotelib("quotes.json")
msg_count = 0
msg_threshold = 20
last_notif = 0
notif_number = 1
commandLastUsed = {}
notStuck = True
for c in inspect.getmembers(commands, inspect.ismodule):
	command = c[1]
	if (hasattr(command, 'check') and inspect.isfunction(command.check)):
		commandLastUsed[command.__name__] = datetime.now() - timedelta(seconds = 10)

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def nameLog():
	dateStr = []
	today = date.today()
	dateStr.append(today)
	logFileName = "logs/" + str(dateStr[0]) + ".txt"
	log = open(logFileName, "a+")
	return log

os.system ("echo '\e[0;32;40m'")

class start_new_thread(threading.Thread):
	def __init__(self, callback, *args, **kwargs):
		threading.Thread.__init__(self)
		self.callback = lambda: callback(*args, **kwargs)
		self.start()

	def run(self):
		self.callback()

def send_data(s,command):
	try:
		print "+ "+command
		s.send(command + "\r\n")
	except (socket.error, socket.timeout):
		print "- INFO - \"%s\" wasn't sent"

def receive_data(command):
	print "- "+command

def send_msg(server, chan, msg):
	incrementUser(chan, "abahbot")
	send_data(server['socket'],"PRIVMSG %s :%s" % (chan, msg))
	print "%s[%s] %s: %s" % (t, chan, NICK, msg)
	log = nameLog()
	log.write("%s[%s] %s: %s\n" % (t, chan, NICK, msg))
	log.close()

def parsemsg(s):
	prefix = ''
	trailing = []
	if s[0] == ':':
		prefix, s = s[1:].split(' ', 1)
	if s.find(' :') != -1:
		s, trailing = s.split(' :', 1)
		args = s.split()
		args.append(trailing)
	else:
		args = s.split()
	command = args.pop(0)
	return prefix, command, args

def get_list(server, chan):
	start_new_thread(update_info, server, chan)
	while (chan in server['CHANNELS']):
		try:
			data = urllib2.urlopen(RAW_CHATTERS % chan[1:])
		except:
			time.sleep(5)
			continue
		userlist = json.load(data)['chatters']
		userlists[hash(chan)] = userlist
		time.sleep(10)
	print "XXXX userlist update thread for %s is dead XXXX\n" % chan

def update_chans(server, chans):
	with open(servers[0]['channelfile'], "w") as f:
		for line in chans:
			f.write(line+"\n")

def is_chatmod(chan, nick):
	try:
		if(nick in userlists[hash(chan)]["moderators"]):
			return 1
		return 0
	except:
		print "USERLIST HASN'T LOADED YETa"
		return 0

def is_broadcaster(chan, nick):
	if(chan[1:].lower() == nick.lower()):
		return 1
	return 0
		
def is_mod(chan, nick):
	try:
		if(nick in userlists[hash(chan)]["moderators"]):
			return 1
		return is_botmod(nick)
	except:
		print "USERLIST HASN'T LOADED YETb"
		return 0
		
def is_viewer(chan, nick):
	try:
		if(nick in userlists[hash(chan)]["viewers"]):
			return 1
		return 0
	except:
		print "USERLIST HASN'T LOADED YETc"
		return 0
		
def is_botmod(nick):
	if(nick in BOTMODS):
		return 1
	return 0

def is_owner(nick):
	if(nick.lower()==OWNER.lower()):
		return 1
	return 0

def is_me(nick):
	if(nick.lower()==NICK.lower()):
		return 1
	return 0

def make_chan(word):
	return word if (word[0] == "#") else "#" + word

def make_not_chan(word):
	return word if (word[0] != "#") else word[1:]

def int_to_roman (integer):

	returnstring=''
	table=[['M',1000],['CM',900],['D',500],['CD',400],['C',100],['XC',90],['L',50],['XL',40],['X',10],['IX',9],['V',5],['IV',4],['I',1]]

	for pair in table:

		while integer-pair[1]>=0:

			integer-=pair[1]
			returnstring+=pair[0]

	return returnstring

def rom_to_int(string):

	table=[['M',1000],['CM',900],['D',500],['CD',400],['C',100],['XC',90],['L',50],['XL',40],['X',10],['IX',9],['V',5],['IV',4],['I',1]]
	returnint=0
	for pair in table:


		continueyes=True

		while continueyes:
			if len(string)>=len(pair[0]):

				if string[0:len(pair[0])]==pair[0]:
					returnint+=pair[1]
					string=string[len(pair[0]):]

				else: continueyes=False
			else: continueyes=False

	return returnint

ignoreList = ['']

def checkCommands(server, chan, nick, msg):
	try:
		if not nick.lower() in ignoreList:
			for c in inspect.getmembers(commands, inspect.ismodule):
				command = c[1]
				if (hasattr(command, 'check') and inspect.isfunction(command.check)):
					if hasattr(command, 'cooldown'):
						if command.cooldown:
								result = command.check(chan, nick, msg, stream_info, is_mod(chan, nick), is_broadcaster(chan, nick), is_botmod(nick))
								if result != None:
									if commandLastUsed[command.__name__] < (datetime.now() - timedelta(seconds = 10)):
										commandLastUsed[command.__name__] = datetime.now()
										send_msg(server,chan, result)
										spamlimit[0] += 1
						else:
							result = command.check(chan, nick, msg, stream_info, is_mod(chan, nick), is_broadcaster(chan, nick), is_botmod(nick))
							if result != None:
								commandLastUsed[command.__name__] = datetime.now()
								send_msg(server,chan, result)
								spamlimit[0] += 1
					else:
						result = command.check(chan, nick, msg, stream_info, is_mod(chan, nick), is_broadcaster(chan, nick), is_botmod(nick))
						if result != None:
							commandLastUsed[command.__name__] = datetime.now()
							send_msg(server,chan, result)
							spamlimit[0] += 1

	except:
		pass
		
def checkCommandsW(server, nick, msg):
	for c in inspect.getmembers(commands, inspect.ismodule):
		command = c[1]
		if (hasattr(command, 'checkW') and inspect.isfunction(command.checkW)):
			result = command.checkW(nick, msg)
			if result != None:
				send_msg(server, server['CHANNELS'][0] , "/w %s %s" % (nick, result))
				spamlimit[0] += 1

def addname(name):
	alias = name[1:]
	lines = json.load(open('lines.json', 'r'))
	if not lines.has_key(name):
		lines[name] = {}
		lines[name]['users'] = {}
		lines[name]["alias"] = alias
		json.dump(lines, open("lines.json","w"), sort_keys=True, indent=4, separators=(',', ': '))

def incrementUser(chan, user):
	addname(chan)
	game = ""
	with open('lines.json', 'r') as f:
		lines = json.load(f)
	result = ""
	if lines.has_key(chan):	
		with open('lines.json', 'w') as f:
			try:
				lines[chan]['users'][user] = lines[chan]['users'][user] + 1
				json.dump(lines, f, sort_keys=True, indent=4, separators=(',', ': '))
				result = "Incrementing User"
			except:
				lines[chan]["users"][user] = 1
				json.dump(lines, f, sort_keys=True, indent=4, separators=(',', ': '))
				result = "User Added"
	else:
		result = "Something happened that shouldn't have happened."
	return result

def bot(server, chan, nick, line):
	global stream_info, msg_count, last_notif, notif_number
	line = line.lower()
	msg = string.split(line, " ")
	msg_count+=1
	chan = chan.lower()
	nick = nick.lower()
	checkCommands(server, chan, nick, msg)
	incrementUser(chan, nick)
	if(msg[0]=="!join" and (chan == "#abahbot" or chan == "#abahbob") and len(msg) == 1):
		chan2 = make_chan("#" + nick)
		if(not chan2 in servers[0]['CHANNELS']):
			send_data(servers[0]['socket'],"JOIN %s" % chan2)
			servers[0]['CHANNELS'].append(chan2)
			update_chans(servers[0], servers[0]['CHANNELS'])
			start_new_thread(get_list,servers[0], chan2)
			send_msg(servers[0],chan, "Entering Channel " + chan2)
		else:
			send_msg(servers[0],chan, "I'm already in " + chan2)
	elif(msg[0]=="!leave" and is_broadcaster(chan, nick)):
		if(len(msg) == 1):
			if(chan in servers[0]['CHANNELS']):
				send_data(servers[0]['socket'],"PART %s" % chan)
				servers[0]['CHANNELS'].remove(chan)
				update_chans(servers[0], servers[0]['CHANNELS'])
				send_msg(servers[0],chan, "Goodbye")
		spamlimit[0] += 1
	elif(msg[0]=="!stats" and (is_broadcaster(chan, nick) or is_botmod(nick))):
		if(len(msg) == 1):
			with open('lines.json', 'r') as f:
				lines = json.load(f)
			result = ""
			if lines.has_key(chan):
				try:
					highest = None
					for user in lines[chan]['users']:
						if highest == None:
							highest = user
						elif lines[chan]['users'][user] > lines[chan]['users'][highest]:
							highest = user
					if highest != None:
						send_msg(server,chan, highest.title() + " has posted the most lines in chat, at " + str(lines[chan]['users'][highest]) + " lines.")
				except:
					pass
			else:
				result = "Something happened that shouldn't have happened."
			return result
		else:
			with open('lines.json', 'r') as f:
				lines = json.load(f)
			result = ""
			if lines.has_key(chan):
				try:
					user = msg[1].lower()
					count = lines[chan]['users'][user]
					send_msg(server,chan, user.title() + " has posted " + str(count) + " lines.")
				except:
					send_msg(server,chan, "User has not posted in chat.")
			else:
				result = "Something happened that shouldn't have happened."
			return result
		spamlimit[0] += 1

def botWhisper(server, nick, line):
	line = line.lower()
	msg = string.split(line, " ")
	nick = nick.lower()
	checkCommandsW(server, nick, msg)
	incrementUser("WHISPER", nick)

def cmd(chan, nick, line):
	line = line.lower()
	msg = string.split(line, " ")
	chan = chan.lower()
	nick = nick.lower()
	if(msg[0]=="!join" and is_botmod(nick) and len(msg) > 1):
		chan2 = make_chan(msg[1])
		if(not chan2 in servers[0]['CHANNELS']):
			send_data(servers[0]['socket'],"JOIN %s" % chan2)
			servers[0]['CHANNELS'].append(chan2)
			update_chans(servers[0], servers[0]['CHANNELS'])
			start_new_thread(get_list, servers[0], chan2)
	elif(msg[0]=="!quit" and is_botmod(nick) and ((chan!="#"+OWNER.lower() and chan!="#"+NICK.lower()) or len(msg)!=1)):
		if(len(msg) == 1):
			if(chan in servers[0]['CHANNELS']):
				send_data(servers[0]['socket'],"PART %s" % chan)
				servers[0]['CHANNELS'].remove(chan)
				update_chans(servers[0], servers[0]['CHANNELS'])
		else:
			chan2 = make_chan(msg[1])
			if(chan2 in servers[0]['CHANNELS'] and chan2!="#"+OWNER.lower() and chan2!="#"+NICK.lower()):
				send_data(servers[0]['socket'],"PART %s" % chan2)
				servers[0]['CHANNELS'].remove(chan2)
				update_chans(servers[0], servers[0]['CHANNELS'])
	elif(msg[0]=="!list" and is_owner(nick)):
		if(len(msg) > 1):
			chan = make_chan(msg[1])
		if (chan in server['CHANNELS']):
			print "staff:"
			print userlists[hash(chan)]["staff"]
			print "admins:"
			print userlists[hash(chan)]["admins"]
			print "moderators:"
			print userlists[hash(chan)]["moderators"]
			print "viewers:"
			print userlists[hash(chan)]["viewers"]
	elif(msg[0]=="!reboot" and is_owner(nick)):
		for se in servers:
			for chan in se['CHANNELS']:
				send_data(se['socket'],"PART %s" % chan)
			while(len(se['CHANNELS']) > 0):
				se['CHANNELS'].pop()
			se['RUN'][0] = 0
			se['socket'].shutdown(socket.SHUT_WR)
			send_data(se['socket'],"QUIT leavin'~")
	elif(msg[0]=="!chans" and is_owner(nick)):
		print "channels:"
		for chans in server['CHANNELS']:
			print " "+chans
	elif(msg[0]=="!test" and is_owner(nick)):
		send_data(server['socket'],"WHO %s" % chan)

def cmdWhisp(nick, line):
	line = line.lower()
	msg = string.split(line, " ")
	nick = nick.lower()
	if(msg[0]=="!test"):
		send_msg(server, server['CHANNELS'][0],"/w %s %s" % (nick, "ayyy lmao"))
	elif(msg[0]=="!join"):
		chan2 = make_chan("#" + nick)
		if(not chan2 in servers[0]['CHANNELS']):
			send_data(servers[0]['socket'],"JOIN %s" % chan2)
			servers[0]['CHANNELS'].append(chan2)
			update_chans(servers[0], servers[0]['CHANNELS'])
			start_new_thread(get_list,servers[0], chan2)
			send_msg(servers[0],chan, "Entering Channel " + chan2)
		else:
			send_msg(server, server['CHANNELS'][0],"/w %s %s %s" % (nick, "I'm already in", chan2))
	elif(msg[0]=="!reboot" and (is_owner(nick) or is_botmod(nick))):
		restart_program()
		for se in servers:
			for chan in se['CHANNELS']:
				send_data(se['socket'],"PART %s" % chan)
			while(len(se['CHANNELS']) > 0):
				se['CHANNELS'].pop()
			se['RUN'][0] = 0
			se['socket'].shutdown(socket.SHUT_WR)
			send_data(se['socket'],"QUIT leavin'~")


def spam_block(server):
	while(server['RUN'][0]):
		time.sleep(5)
		if(spamlimit[0] > 0):
			spamlimit[0] -= 1
	print "XXXX Spam block is dead XXXX\n"

def update_info(server, chan):
	if chan [1] != "_":
		global stream_info
		while server['RUN'][0]:
			try:
				result = urllib2.urlopen(CHANNEL_API + chan[1:])
				stream_info[chan] = json.load(result)
			except:
				print("Error loading stream info, restarting")
				restart_program()
				for se in servers:
					for chan in se['CHANNELS']:
						send_data(se['socket'],"PART %s" % chan)
					while(len(se['CHANNELS']) > 0):
						se['CHANNELS'].pop()
					se['RUN'][0] = 0
					se['socket'].shutdown(socket.SHUT_WR)
					send_data(se['socket'],"QUIT leavin'~")
			time.sleep(2)
		print "XXXX Stream Info Thread is Dead XXXX\n"
	
def check_connection (socket):
	while server['is_alive'][0] == 0:
		continue
	connected = 1
	while (connected and server['is_alive'][0]):
		time.sleep(60)
		ping_time = time.time()
		print "atashi no pingu~"
		try:
			socket.send("PING tsundere\r\n")
		except:
			print "ping failed"
			break
		while (time.time() - ping_time < threshold and server['is_alive'][0]):
			connected = 0
			if server['PING'][0]:
				pong_time= time.time() - ping_time 
				print "response time %fs" % pong_time 
				server['PING'][0] = 0
				connected = 1
				break
	connected = 001
	server['is_alive'][0] = 0
	start_new_thread(check_connection,socket)

def join_server(server):
	server['readbuffer'] = ""
	while 1:
		server['RUN'][0] = 1
		server['is_alive'][0] = 0
		start_new_thread(spam_block, server)

		with open(server['channelfile']) as f:
			server['CHANNELS'] = f.read().splitlines()

		while server['is_alive'][0] == 0:
			server['socket']=socket.socket()
			try:
				server['socket'].connect((server['HOST'], server['PORT']))
				server['socket'].setblocking(0)
				send_data(server['socket'], "PASS %s" % PASS)
				send_data(server['socket'], "NICK %s" % NICK)
				send_data(server['socket'], "USER %s 0 * :%s" % (NICK, OWNER))
				for chan in server['CHANNELS']:
					send_data(server['socket'],"JOIN %s" % chan)
					if chan[1] == '_':
						send_data(server['socket'], 'CAP REQ :twitch.tv/commands')
					time.sleep(.3)
				server['is_alive'][0] = 1
			except:
				server['socket'].close()
				os.system ("echo '\e[0;37;44m'")
				print "++++++++++++++ connection failed, retrying in 5s"
				time.sleep(5)
				continue

		for chan in server['CHANNELS']:
			start_new_thread(get_list, server, chan)

		os.system ("echo '\e[0;32;40m'")
		print "-------------- connected"
		t = datetime.now().strftime("%H:%M:%S on %B %d, %Y")
		print "session start at %s" % (t)
		#start_new_thread(check_connection)

		server['RUN'][0] = 1
		server['is_alive'][0] = 0
		print(server['HOST'])
		start_new_thread(spam_block, server)

		with open(server['channelfile']) as f:
			server['CHANNELS'] = f.read().splitlines()

		for chan in server['CHANNELS']:
			start_new_thread(get_list, server, chan)

		while server['RUN'][0]:
			try:
				server['readbuffer']=server['readbuffer']+server['socket'].recv(1024)
				#if is_alive[0] == 0:
					#raise socket.timeout("missing pong")
			except (socket.error, socket.timeout):
				server['readbuffer']=""
				server['socket'].close()
				server['socket']=socket.socket()
				try:
					server['socket'].connect((server['HOST'], server['PORT']))
					send_data(server['socket'],"PASS %s" % PASS)
					send_data(server['socket'],"NICK %s" % NICK)
					send_data(server['socket'],"USER %s 0 * :%s" % (NICK, OWNER))
					for chan in server['CHANNELS']:
						send_data(server['socket'],"JOIN %s" % chan)
						if chan[1] == '_':
							send_data(server['socket'], 'CAP REQ :twitch.tv/commands')
						time.sleep(.3)
					print "-------------- reconnected\n"
					#is_alive[0] = 1
					os.system ("echo '\e[0;32;40m'")
				except (socket.error, socket.timeout):
					print "++++++++++++++ reconnection failed retrying in 5s"
					time.sleep(5)
					continue
				continue
			except Exception, e:
				print e
				time.sleep(5)
				continue
			temp=string.split(server['readbuffer'], "\r\n")
			server['readbuffer']=temp.pop()
			t = datetime.now().strftime("[%H:%M:%S]")

			for line in temp:
				prefix, command, params = parsemsg(line)
				nick = string.split(prefix,"!")
				
				if(command=="PING"):
					#print t
					#print "anata no pingu~"
					data = params.pop(0)
					#print "atashi no pongu~"
					try:
						server['socket'].send("PONG :%s\r\n" % data)
					except socket.error, socket.timeout:
						print "- INFO - \"atashi no pongu~\" wasn't sent"
				#elif(command=="PONG"):
					#print "anata no pongu~"
					#PING[0] = 1
				elif(command=="PRIVMSG"):
					chan = params.pop(0)
					msg = params.pop(0)
					msg = msg.rstrip()
					if (nick[0]!="jtv"):
						chan_rights = "@" if is_chatmod(chan, nick[0]) else "" 
						bot_rights = "$" if is_botmod(nick[0]) else "" 
					print "%s[%s] %s%s%s: %s" % (t, chan, bot_rights, chan_rights, nick[0], msg)
					log = nameLog()
					log.write("%s[%s] %s%s%s: %s\n" % (t, chan, bot_rights, chan_rights, nick[0], msg))
					log.close()
					if(spamlimit[0] < 5):
						bot(server, chan, nick[0], msg)
					cmd(chan, nick[0], msg)
				elif(command=="WHISPER"):
					msg = params.pop(1)
					msg = msg.rstrip()
					print "%s[%s] %s: %s" % (t, "WHISPER", nick[0], msg)
					log = nameLog()
					log.write("%s[%s] %s: %s\n" % (t, "WHISPER", nick[0], msg))
					log.close()
					botWhisper(server, nick[0], msg)
					cmdWhisp(nick[0], msg)
				elif(command=="JOIN"):
					chan = params.pop(0)
					print "%s joined [%s]" % (nick[0], chan)
				elif(command=="PART"):
					chan = params.pop(0)
					print "%s left [%s]" % (nick[0], chan)
				elif(command=="MODE"):
					chan = params.pop(0)
					nick = params.pop(1)
					mode = params.pop(0)
					print "[%s] gives %s to %s" % (chan, mode, nick)
				elif(command=="001"):
					print "welcome: %s" % params[1]
				elif(command=="002"):
					print "host: %s" % params[1]
				elif(command=="003"):
					print "creation date: %s" % params[1]
				elif(command=="004"):
					print "my info: %s" % params[1]
				elif(command=="375"):
					print "______________________________"
					print params[1]
				elif(command=="376"):
					print params[1]
					print "______________________________"
				elif(command=="372"):
					print "%s" % params[1]
				elif(command=="315"):
					print "end of /WHO for [%s]" % params[1]
				elif(command=="353"):
					print "receiving /NAMES for [%s]: %s" % (params[2],params[3])
				elif(command=="366"):
					print "end of /NAMES for [%s]" % params[1]
				elif(command=="421"):
					print "unknown command: %s" % params[1]
				elif(command=="RECONNECT"):
					for chan in server['CHANNELS']:
						send_data(server['socket'],"PART %s" % chan)
					while(len(server['CHANNELS']) > 0):
						server['CHANNELS'].pop()
					server['RUN'][0] = 0
					server['socket'].shutdown(socket.SHUT_WR)
					send_data(server['socket'],"QUIT leavin'~")
				else:
					receive_data(line)
		print "sleeping for 5s"
		time.sleep(5)


for server in servers:
	start_new_thread(join_server,server)
