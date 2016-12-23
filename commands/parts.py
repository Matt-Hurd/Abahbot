games = ["Borderlands 2", "Borderlands: The Handsome Collection"]
def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if((msg[0]=="!parts" or msg[0]=="!gunparts") and stream_info[chan]["game"] in games):
		return("BOOM GUN PARTS http://imgur.com/a/eIXvz#0")

def checkW(nick, msg):
	if(msg[0]=="!parts" or msg[0]=="!gunparts"):
		return("BOOM GUN PARTS http://imgur.com/a/eIXvz#0")