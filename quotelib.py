import json, random

class quotelib:
	def __init__(self, path=None):
		if path == None:
			print "usage: quotelib.quotelib(<path to json file>"
			return None
		self._path = path
		self._jso = json.load(open(path,"r"))
		return None
		
	def printall(self):
		for name in self._jso:
			for quote in self._jso[name]["quotes"]:
				print quote["quote"]
		return None
	
	#!quote <name> -> quotelib.quote(name)
	def quote(self, name=None, rng=None):
		#quote()
		if name:
			name = name.title()
		else:
			name = random.choice(self._jso.keys())
		
		#quote(name)
		if self._jso.has_key(name):
			quotes = self._jso[name]["quotes"]
			#quote(name)
			if rng == None:
				if len(quotes) > 1:
					rng = random.randrange(len(self._jso[name]["quotes"]))
				else:
					rng = 0
			#quote(name, rng)
			else:
				rng = (rng - 1) % len(quotes)
			return "\"%s\" - %s %s" % (quotes[rng]["quote"], self._jso[name]["alias"], quotes[rng]["year"])
		return "I don't know this %s person, and that's a creepy name anyway!" % name
	
	def addquote(self, name, quote, year):
		name = name.title()
		if self._jso.has_key(name):
			self._jso[name]["quotes"].append({"quote":quote, "year":year})
			json.dump(self._jso,open(self._path,"w"))
		else:
			print "wrong name: %s", name
		return None
	
	def addname(self, name, alias):
		name = name.title()
		if self._jso.has_key(name):
			print "name \"%s\"already registered" % name
		else:
			self._jso[name.title()] = {}
			self._jso[name.title()]["quotes"] = []
			self._jso[name.title()]["alias"] = alias
			json.dump(self._jso,open(self._path,"w"))
		return None
	
	def quantity(self, name):
		name = name.title()
		if self._jso.has_key(name):
			return len(self._jso[name]["quotes"])
		print "wrong name: %s" % name
		return 0