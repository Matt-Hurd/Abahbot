import json

def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!shining"):
		misc = json.load(open('misc.json', 'r'))
		if(is_mod):
			count = misc["Shining"]
			misc["Shining"] = count + 1
			json.dump(misc, open("misc.json","w"), sort_keys=True, indent=4, separators=(',', ': '))
			return("Shining has been damned " + str(count + 1) + " times.")

def checkW(nick, msg):
	if(msg[0]=="!shining" or msg[0]=="shining"):
		misc = json.load(open('misc.json', 'r'))
		count = misc["Shining"]
		misc["Shining"] = count + 1
		json.dump(misc, open("misc.json","w"), sort_keys=True, indent=4, separators=(',', ': '))
		return("Shining has been damned " + str(count + 1) + " times.")
	elif nick.lower() == "shiningface":
		return("Dammit Shining")