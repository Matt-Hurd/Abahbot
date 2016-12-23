import urllib2
import json
import datetime

STREAM_API = 'https://api.twitch.tv/kraken/streams/'

def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!uptime"):
		try:
			with contextlib.closing(urllib2.urlopen(STREAM_API + chan[1:])) as x:
				stream = json.load(x)
			startTimeStr = stream["stream"]["created_at"]
			startTimeDT = datetime.datetime.strptime(startTimeStr, "%Y-%m-%dT%H:%M:%SZ")
			uptime = datetime.datetime.now() + datetime.timedelta(hours=4) - startTimeDT
			return 'The stream has been up for %d hours, %d minutes, and %d seconds.' % (uptime.seconds/3600, uptime.seconds%3600/60, uptime.seconds%60)
		except:
			return