def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!color" and is_botmod(nick) and len(msg) > 1):
		return("/color %s" % msg[1])