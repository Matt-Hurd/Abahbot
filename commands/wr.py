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
import os
import linecache
import inspect
import commands
import contextlib
from datetime import datetime, timedelta

WORLD_RECORDS_API = 'http://www.speedrun.com/api_records.php?game='

aliases = {"borderlands: the pre-sequel!" : "borderlands: the pre-sequel",
		   "the legend of zelda: the wind waker" : "tww"}
categoryFixes =  {"borderlands 2" : "Any% w/DLC"}


def getWR(game, category):
	mainIsLoadless = False
	game = game.rstrip().lstrip().lower()
	try:
		for g in aliases:
			if game == g:
				game = aliases[g]
		if (category == "any%"):
			print "a"
			for c in categoryFixes:
				if game == c:
					print "c"
					category = categoryFixes[c]
		url = (WORLD_RECORDS_API + game).rstrip().replace(' ',"%20")
		print url
		category = category.rstrip().lstrip()
		with contextlib.closing(urllib2.urlopen(url)) as x:
			result = json.load(x)
		times = result[result.keys()[0]]
		time = -1
		for key in times.keys():
			try:
				times[key]["timeigt"]
				timeKey = 'timeigt'
			except:
				timeKey = 'time'
			try:
				times[key]["timewithloads"]
				mainIsLoadless = True
				if times[key][timeKey] == None:
					timeKey = "timewithloads"
					mainIsLoadless = False
			except:
				pass
			if "any%" in category.lower():
				if "any%" in key.lower() and not "ng+" in key.lower():
					print times[key][timeKey]
					if(time == -1 or time > float(times[key][timeKey])):
						important_time = times[key]
						cate = key
						time = float(times[key][timeKey])
			elif (' ' in category):
				words = category.split(' ')
				if all(word in str.lower(str(key)) for word in words):
					if(time == -1 or length == -1 or len(key) < length):
						length = len(key)
						important_time = times[key]
						cate = key
						time = float(times[key][timeKey])
			elif str.lower(str(category)) in str.lower(str(key)):
				if(time == -1 or length == -1 or len(key) < length):
					length = len(key)
					important_time = times[key]
					cate = key
					time = float(times[key][timeKey])
		playerStr = ""
		try:
			important_time
		except:
			for key in times.keys():
				try:
					times[key]["timeigt"]
					timeKey = 'timeigt'
				except:
					timeKey = 'time'
				try:
					times[key]["timewithloads"]
					mainIsLoadless = True
					if times[key][timeKey] == None:
						timeKey = "timewithloads"
						mainIsLoadless = False
				except:
					pass
				print times[key][timeKey]
				if(time == -1 or time > float(times[key][timeKey])):
					important_time = times[key]
					cate = key
					time = float(times[key][timeKey])

		try:
			players = []
			players.append(important_time["player"])
			for num in range(2,100):
				players.append(important_time["player" + str(num)])
		except:
			for player in players:
				if player == players[-1] and len(players) > 1:
					playerStr+="and "
				playerStr+=player
				if len(players) > 2: 
					if player != players[-1]:
						playerStr+=", "
				else:
					playerStr+=" "
		timingStr = '' if (timeKey == 'time') and not mainIsLoadless else ' (IGT)'
		link = important_time['links']['web']
		return cate + " in " + str(timedelta(seconds=int(time))) + " by " + playerStr + timingStr + ': ' + link
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
   		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
   		print(exc_type, fname, exc_tb.tb_lineno)
		return "Record not found"

def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!wr"):
		category = ""
		if(len(msg) == 1):
			return(getWR(stream_info[chan]["game"], "any%"))
		elif(len(msg) == 2):
			return(getWR(stream_info[chan]["game"], msg[1]))
		elif(len(msg) >= 3):
			a = " ".join(msg)
			if('|' in a):
				b = a.split('|')
				return(getWR(b[0][4:],b[1]))
			else:
				print a[4:]
				return(getWR(a[4:], "any%"))

def checkW(nick, msg):
	if(msg[0]=="!wr" or msg[0]=="wr"):
		modifier = 0
		if (msg[0] == "!"):
			modifier = 1
		category = ""
		if(len(msg) == 1):
			return("Give me a game!")
		elif(len(msg) == 2):
			return(getWR(msg[1], "any%"))
		elif(len(msg) >= 3):
			a = " ".join(msg)
			if('|' in a):
				b = a.split('|')
				return(getWR(b[0][3 + modifier:],b[1]))
			else:
				return(getWR(a[3 + modifier:], "any%"))	