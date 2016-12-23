def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!pat"):
		if(is_botmod):
			return("%s-senpai <3" % nick.title())