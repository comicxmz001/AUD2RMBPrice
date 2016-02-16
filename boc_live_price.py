#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import html
from six.moves import urllib
import threading
import time

class RMB2AUD(object):
	"""docstring for RMB2AUD"""
	def __init__(self, root):
		self.thtml = root
	def getPrice(self, timestep = 0):
		tpublish = self.thtml.find_class("publish")[0]
		# get the div that wraps currency rates table, which has not class
		for div in tpublish.iterchildren(tag="div"):
			if not len(div.values()):
				table = div.findall("table")[0]
				trs = table.findall("tr")
				ths = trs[0].getchildren()
				for tr in trs[1:]:
					if tr.find("td").text.encode('utf-8') == "澳大利亚元":
						currency = tr.findall("td")
						AUD = {}
						AUD["name"] = currency[0].text.encode('utf-8')
						AUD["price"] = currency[3].text
						AUD["date"] = currency[-2].text
						AUD["time"] = currency[-1].text
						print "{name} ({date} {time}) = {price}".format(name=AUD["name"],date=AUD["date"],time=AUD["time"],price=AUD["price"])
		if timestep:
			time.sleep(timestep)
			self.getPrice(timestep)
		return AUD["price"]
	def repeat(self, timestep):
		# repeat every timestep seconds
		self.getPrice(timestep)
		threading.Timer(timestep,self.repeat).start()

if __name__ == '__main__':
	# parse from local files
	# tree = html.parse("boc.html")
	# thtml = tree.getroot()
	
	# parse from live site
	tree = html.fromstring(urllib.request.urlopen("http://www.boc.cn/sourcedb/whpj/").read())
	thtml = tree
	AUD = RMB2AUD(thtml)
	AUD.getPrice(60)

	
	

