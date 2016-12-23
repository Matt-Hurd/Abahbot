def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!title" and is_mod):
		return stream_info[chan]["status"]