import json

def check(chan, nick, msg, stream_info, is_mod, is_broadcaster, is_botmod):
	if(msg[0]=="!faq"):
		with open('FAQs.json', 'r') as f:
			FAQs = json.load(f)
		print 'test'
		if len(msg) > 1:
			try:	
				game = ""
				for word in msg[1:]:
					game = game + word + " "
				game = game.rstrip()
				print game
				FAQ = FAQs[chan]['games'][0][game.lower()]
				return game.title() + " FAQ: " + FAQ
			except:
				return "No FAQ found."
		else:
			try:
				FAQ = FAQs[chan]['titles'][0]
				for gametitle in FAQ:
					if str.lower(str(gametitle)) in str.lower(str(stream_info[chan]['status'])):		
						return gametitle.title() + " FAQ: " + FAQ[gametitle]
					FAQ = FAQs[chan]['games'][0][stream_info[chan]["game"].lower()]
					return stream_info[chan]["game"] + " FAQ: " + FAQ
			except:
				return "No FAQ found."
