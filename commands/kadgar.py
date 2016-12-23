import re,json

games = ["Borderlands 2"]
channels = ["#thefuncannon", "#shiningface", "#abahbob", "#blackwayv"]
titleContains = "co-op"
cooldown = True
def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!kadgar" and stream_info[chan]["game"] in games and chan in channels and titleContains in stream_info[chan]["status"].lower()):
		return("http://kadgar.net/live/shiningface/thefuncannon/abahbob/blackwayv")
	elif((msg[0]=="!multitwitch" or msg[0]=="!multi") and stream_info[chan]["game"] in games and chan in channels and titleContains in stream_info[chan]["status"].lower()):
		return("http://multitwitch.tv/abahbob/shiningface/thefuncannon/blackwayv")
	elif(msg[0]=="!speedruntv" and stream_info[chan]["game"] in games and chan in channels and titleContains in stream_info[chan]["status"].lower()):
		return("http://speedrun.tv/abahbob/thefuncannon/shiningface/blackwayv")