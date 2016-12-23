import re,json

games = ["Borderlands 2", "Borderlands: The Handsome Collection"]
cooldown = True
def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!vladof" and stream_info[chan]["game"] in games):
		return(" By merging the free shot of vladof launchers, you can make weapons use one less ammo per shot. However, on patch 1.3 and below, you can stack the vladof launchers effect infinitly to make every weapon consume 0 ammo per shot. Merging, and therefore infinite ammo, has been fixed on current patch for both BL2 and TPS.")		
	else:
		lines = json.load(open('lines.json', 'r'))
		result = ""
		posts = 0
		if lines.has_key(chan):
			try:
				posts = lines[chan]['users'][nick]
			except:
				pass
		else:
			result = "Something happened that shouldn't have happened."
		if posts < 4 and re.match("(how|why).*((not|don'{0,1}t) (consume|use|spend)|run out of|unlim|inf).+(ammo|mag|rocket)", ' '.join(msg)):
			return("@" + nick + ",  by merging the free shot of vladof launchers, you can make weapons use one less ammo per shot. However, on patch 1.3 and below, you can stack the vladof launchers effect infinitly to make every weapon consume 0 ammo per shot. Merging, and therefore infinite ammo, has been fixed on current patch for both BL2 and TPS.")

def checkW(nick, msg):
	if(msg[0]=="!vladof"):
		return(" By merging the free shot of vladof launchers, you can make weapons use one less ammo per shot. However, on patch 1.3 and below, you can stack the vladof launchers effect infinitly to make every weapon consume 0 ammo per shot. Merging, and therefore infinite ammo, has been fixed on current patch for both BL2 and TPS.")