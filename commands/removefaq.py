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

def removefaq(name, gameArray):
	addname(name)
	game = ""
	for word in gameArray:
		game = game + word + " "
	game = game.rstrip()
	with open('FAQs.json', 'r') as f:
		FAQs = json.load(f)
	if FAQs.has_key(name):
		try:
			del FAQs[name]['games'][0][game]
			with open('FAQs.json', 'w') as f:
				json.dump(FAQs, f, sort_keys=True, indent=4, separators=(',', ': '))
			return("FAQ Removed")
		except:
			return("No FAQ exists for this game.")
	else:
		return("Something happened that shouldn't have happened.")
	return None

def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!removefaq" and is_mod and len(msg) > 1):
		return removefaq(chan, msg[1:])