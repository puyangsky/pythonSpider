import urllib
import urllib2
import re
import thread
import time

class QSBK:
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		self.headers = { 'User-Agent' : self.user_agent }
		self.stories = []
		self.enable = False

	def getPage(self, pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			req = urllib2.Request(url, headers = self.headers)
			res = urllib2.urlopen(req)
			content = res.read().decode('utf-8')
			return content
		except urllib2.URLError, e:
			if hasattr(e,"code"):
				print e.code
			if hasattr(e, "reason"):
				print e.reason

	def getPageItems(self, pageIndex):
		content = self.getPage(pageIndex)
		if not content:
			print "Failed loading page..."
			return None
		pattern = re.compile('<div.*?author clearfix">.*?<a.*?<img.*?alt="(.*?)"/>.*?<div.*?content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
		items = re.findall(pattern, content)
		pageStories = []
		for item in items:
			haveImg = re.search("img", item[3])
			if not haveImg:
				replaceBR = re.compile('<br/>')
				text = re.sub(replaceBR, "\n", item[1])
				pageStories.append([item[0].strip(), text.strip(), item[2].strip(), item[4].strip()])
		return pageStories		

	def loadPage(self):
		if self.enable == True:
			print "length of stories:%d" % len(self.stories)
			# print self.stories
			if len(self.stories) < 1:
				pageStories = self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex += 1

	def getOneStory(self, pageStories, page):
		for story in pageStories:
			input = raw_input()
			self.loadPage()
			if input == "Q":
				self.enable = False
				return
			print u"page:%d\tauthor:%s\ttime:%s\tzan:%s\n%s" % (page,story[0],story[2],story[3],story[1])

	def start(self):
		print u"print Enter for new story, Q for quit"
		self.enable = True
		self.loadPage()
		nowPage = 0
		while self.enable:
			if len(self.stories) > 0:
				pageStories = self.stories[0]
				nowPage += 1
				del self.stories[0]
				self.getOneStory(pageStories, nowPage)

spider = QSBK()
spider.start()









