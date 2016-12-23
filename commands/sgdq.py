def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!sgdq" or msg[0]=="!gdq" or msg[0]=="!agdq"):
		return("Games Done Quick is a series of charity video game marathons. These events feature high-level play by speedrunners raising money for charity. https://gamesdonequick.com/ ")


def checkW(nick, msg):
	return check('', nick, msg, '', '', '', '')