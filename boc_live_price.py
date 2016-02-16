#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import html
from six.moves import urllib
import threading
import time
import datetime

class RMB2AUD(object):
	"""docstring for RMB2AUD"""
	def __init__(self):
		print "Process starts at %s" %datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
	def getPrice(self, timestep = 0):
		thtml = html.fromstring(urllib.request.urlopen("http://www.boc.cn/sourcedb/whpj/").read())
		tpublish = thtml.find_class("publish")[0]
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
						# AUD["name"] = currency[0].text.encode('utf-8')
						AUD["name"] = "AUD"
						AUD["price"] = currency[3].text
						AUD["date"] = currency[-2].text
						AUD["time"] = currency[-1].text
						currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
						print "[{ctime}]: 1 {name} = {price} RMB ({date} {time}) ".format(ctime=currentTime,name=AUD["name"],date=AUD["date"],time=AUD["time"],price=AUD["price"])
		if timestep:
			time.sleep(timestep)
			self.getPrice(timestep)
		return AUD["price"]

if __name__ == '__main__':
	AUD = RMB2AUD()
	AUD.getPrice(60)

	
	

