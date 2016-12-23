def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!twitter" and is_mod and chan == "#thefuncannon"):
		return "FunCannon's Twitter: https://twitter.com/TheFuncannon"	
	elif(msg[0]=="!twitter" and is_mod and chan == "#abahbob"):
		return "Abahbob's Twitter: https://twitter.com/Abahbob"