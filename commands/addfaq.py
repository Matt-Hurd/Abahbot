import json

def addname(name):
	alias = name[1:]
	with open('FAQs.json', 'r') as f:
		FAQs = json.load(f)
	if FAQs.has_key(name):
		print("name \"%s\"already registered" % name)
	else:
		FAQs[name] = {}
		FAQs[name]['games'] = [{}]
		FAQs[name]['titles'] = []
		FAQs[name]["alias"] = alias	
		with open('FAQs.json', 'w') as f:
			json.dump(FAQs, f, sort_keys=True, indent=4, separators=(',', ': '))

def addfaq(name, gameArray, url):
	addname(name)
	game = ""
	for word in gameArray:
		game = game + word + " "
	game = game.rstrip().lower()
	with open('FAQs.json', 'r') as f:
		FAQs = json.load(f)
	result = ""
	if FAQs.has_key(name):
		try:
			FAQs[name]['games'][0][game]
			result = "An FAQ for this game already exists"
		except:
			FAQs[name]["games"][0][game] = url
			with open('FAQs.json', 'w') as f:
				json.dump(FAQs, f, sort_keys=True, indent=4, separators=(',', ': '))
			result = "FAQ Added"
	else:
		result = "Something happened that shouldn't have happened."
	return result

def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!addfaq" and is_mod):
		if(len(msg) == 2):
			return addfaq(chan, [stream_info[chan]["game"].lower()], msg[1])
		elif(len(msg) > 2):
			return addfaq(chan, msg[1:-1], msg[-1:][0])