def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!bq"):
		return("Beta Quest (an OOT mod created by Mzxrules) modifies all entrances to load a randomized area instead of the correct one, with the filename used as the seed to shuffle all possible entrances. For bingos, the bingo card seed is also used as the filename. Further information and other changes can be found here: http://forums.zeldaspeedruns.com/index.php?topic=2032.0")