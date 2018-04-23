# !/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
from lxml import etree
import time
import os

"""
此功能由于反爬虫机制尚未解决，所以暂停
def homePage(url):
	html = dealPage(url)
	content = etree.HTML(html)
	#print(content)
	page_list = content.xpath('//a[@class="page-numbers"]/text()')
	print(page_list)
	num = page_list[-1]
	num = int(num)
	for i in range(1, num+1):
		homePageurl = "http://www.mzitu.com/page/" + str(i)
		loadPage(homePageurl)
"""



def dealPage(url):
    """此方法专门用来发送请求，并读取返回的响应内容"""
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
'Referer':'http://i.meizitu.net'}
	request = urllib.request.Request(url, headers=headers)
	response = urllib.request.urlopen(request)
	html = response.read()
	return html

def loadPage(url):
	html = dealPage(url)
	# 返回的是HTML DOM模型
	content = etree.HTML(html)
	link_list = content.xpath('//li/a[@target="_blank"]/@href')
	page_list = content.xpath('//a[@class="page-numbers"]/text()')
	#print(len(link_list))
	num = page_list[-1]
	num = int(num)
	for i in range(1, num+1):
		for link in link_list:
			loadSetPage(link)

def loadSetPage(link):
	html = dealPage(link)
	content = etree.HTML(html)
	link_list = content.xpath('//p/a/img/@src')
	page_list = content.xpath('//div[@class="pagenavi"]/a/span/text()')
	if len(page_list) >= 2:
		num = page_list[-2]
		#print(num)
		num = int(num)
		link = link_list[0]
		for i in range(1, num+1):
			if i < 10:
				fullLink = link[:-5] + str(i) + ".jpg"
				writePage(fullLink)
#				print(fullLink)
			else:
				fullLink = link[:-6] + str(i) + ".jpg"
				writePage(fullLink)
#				print(fullLink)
			print("---------finish--------")

def writePage(link):
	image = dealPage(link)
	fileName = link[-9:]
	if os.path.exists(fileName) == False:
		with open(fileName, "wb") as f:
			f.write(image)
	else:
		print("---------跳过--------")

if __name__ == '__main__':
	url = "http://www.mzitu.com/"
	homePage(url)
