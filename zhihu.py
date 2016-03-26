import requests
import re

def getContent(url):
	r = requests.get(url)
	return r.content

def getXSRF(url):
	content = getContent(url)
	pattern = re.compile('.*?<input type="hidden" name="_xsrf" value="(.*?)"/>.*?')
	match = re.findall(pattern, content)
	xsrf = match[0]
	# m = pattern.match(content)
	# print m.group()
	return xsrf
def login(baseurl,email,password):
    login_data = {
    		'_xsrf': getXSRF(baseurl),
    		'password': password,
    		'remember_me': 'true',
    		'email': email,
    }
    headers_base = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
		'Connection': 'keep-alive',
		'Host': 'www.zhihu.com',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', 
		'Referer': 'http://www.zhihu.com/',
	}

    session = requests.session()
    baseurl += "/login/email"
    content = session.post(baseurl, headers = headers_base, data = login_data)
    print content
    s = session.get("http://www.zhihu.com", verify = False)
    print s.text.encode('utf-8')
    f = open('zhihu.txt', 'w')
    f.write(s.text.encode('utf-8'))
url = "http://www.zhihu.com"

login(url,"******@***.com","************")
