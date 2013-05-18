import sys
import os
import re
import urllib2
import urlparse


if len(sys.argv) < 2:
  print("Error: No start url was passed")
	sys.exit()


tocrawl = set([sys.argv[1]])
crawled = set([])
keywordregex = re.compile('<meta\sname=["\']keywords["\']\scontent=["\'](.*?)["\']\s/>')
linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')

while 1:
	try:
		crawling = tocrawl.pop()
		print crawling
		scr="python PR.py "
		scr=scr+crawling
		#os.system(scr)    
	except KeyError:
		raise StopIteration
	url = urlparse.urlparse(crawling)
	try:
		response = urllib2.urlopen(crawling)
	except:
		continue
	msg = response.read()
	startPos = msg.find('<title>')
	if startPos != -1:
		endPos = msg.find('</title>', startPos+7)
		if endPos != -1:
                                                      fileName, ext = os.path.splitext(crawling)
                                                      #print "EXT:",ext
                                                      if ext!="flv" and  ext!="avi" and ext!="aac" and ext!="mp3":
                                                              title = msg[startPos+7:endPos]
                                                              title=title.lower()
                                                              title = title.replace("|", "")
                                                              title = title.replace("-", "")
                                                              title = title.replace("&", "")
                                                              #print title
                                                              scr1="python TE.py "
                                                              scr1=scr1+crawling
                                                              scr1=scr1+" "
                                                              scr1=scr1+title
                                                              #print "\n"
                                                              #print scr1
                                                              os.system(scr1)


	
	links = linkregex.findall(msg)
	crawled.add(crawling)
	for link in (links.pop(0) for _ in xrange(len(links))):
		if link.startswith('/'):
			link = 'http://' + url[1] + link
		elif link.startswith('#'):
			link = 'http://' + url[1] + url[2] + link
		elif not link.startswith('http'):
			link = 'http://' + url[1] + '/' + link
		if link not in crawled:
			tocrawl.add(link)
