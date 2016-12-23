def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!tip"):
		if(is_botmod or nick == "blackwayv"):
			return("M'Lady")