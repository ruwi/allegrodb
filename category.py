#-*- coding: utf-8 -*-

from HTMLParser import HTMLParser

class CategoryParser(HTMLParser):
	def __init__(self,*args,**argv):
		self.n = 0
		HTMLParser(self,*args,**argv)
		
	def handle_starttag(self,tag,attrs):
		for i in range(1,5):
			if tag == 'a' and ('class', "alleLink lvl" + str(i)) in attrs:
				self.n=1
				self.lvl=i

	def handle_endtag(self,tag):
		if self.n == 1 and tag == 'a':
			self.n = 0
			self.lvl = -1

	def handle_data(self,data):
		if self.n == 1:
			self.title = data
		if self.n == 2:
			self.quantity
