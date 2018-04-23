# !/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
from lxml import etree
import time
import os
import random

def dealPage(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
'Referer':'http://i.meizitu.net'}
	request = urllib.request.Request(url, headers=headers)
	t = random.uniform(0.1, 0.5)
	time.sleep(t)
	response = urllib.request.urlopen(request)
	html = response.read()
	return html

def loadPage(url):
	html = dealPage(url)
	# 返回的是HTML DOM模型
	content = etree.HTML(html)
	link_list = content.xpath('//li/a[@target="_blank"]/@href')
	j = 1
	for link in link_list:
		loadSetPage(link, j)
		j += 1

def loadSetPage(link, j):
	html = dealPage(link)
	content = etree.HTML(html)
	dir_name = content.xpath('//div[@class="content"]/h2/text()')
	link_list = content.xpath('//p/a/img/@src')
	page_list = content.xpath('//div[@class="pagenavi"]/a/span/text()')
	if len(page_list) >= 2:
		num = page_list[-2]
		num = int(num)
		link = link_list[0]
		path = "./image/" + dir_name[0]
		isExists = os.path.exists(path)
		if not isExists:
			try:
				os.makedirs(path)
			except:
				print("error")
				path = "./image"
			for i in range(1, num+1):
				if i < 10:
					fullLink = link[:-5] + str(i) + ".jpg"
					writePage(fullLink, i, path)
				else:
					fullLink = link[:-6] + str(i) + ".jpg"
					writePage(fullLink, i, path)
			print("---------finish%d--------"%j)
		
		else:
			print(path + " :已存在")
			

def writePage(link, i, path):
	image = dealPage(link)
	fileName = path + "/" + link[-12:-11] + link[-9:]
	if os.path.exists(fileName) == False:
		with open(fileName, "wb") as f:
			f.write(image)

if __name__ == '__main__':
	i = int(input("请输入要开始爬取的页码："))
	while True:
		url = "http://www.mzitu.com/page/" + str(i)
		loadPage(url)
		print("第%d页下载完成"%i)
		s = input("退出(quit),继续(任意键):")
		if s == "quit":
			break
		else:
			i += 1
