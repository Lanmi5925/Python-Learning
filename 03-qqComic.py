# !/usr/bin/env python3
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
from lxml import etree
import random
import os


def loadPage(url, i, n):
	browser.get(url)
	t = random.uniform(0.5, 0.6)
	time.sleep(t)
	# 先找到一幅未加载漫画的图片位置
	targets = browser.find_elements_by_xpath('//div/ul/li[@style]/img[@src="//ac.gtimg.com/media/images/pixel.gif"]')
	try:
		target = targets[0]
	except:
		print("没有此页面")
		return n
	while target:
		# 不断跳转到未加载图片位置，让漫画加载出来
		browser.execute_script("arguments[0].scrollIntoView();", target)
		targets = browser.find_elements_by_xpath('//div/ul/li[@style]/img[@src="//ac.gtimg.com/media/images/pixel.gif"]')
		# 判断是否全部加载完毕
		if len(targets) == 0:
			break
		target = targets[0]
	time.sleep(t)
	xpath = '//div/ul/li[@style]/img'
	comicLinks = browser.find_elements_by_xpath(xpath)
	path = "./Comic/episode" + str(n)
	j = 1 # 用来给下载的每一章节的图片命名，计数
	isExists = os.path.exists(path)
	if not isExists:
		try:
			os.makedirs(path)
		except:
			print("error")
			path = "./image/errorFile"
		for element in comicLinks:
			img_url = element.get_attribute('src')
			#print(img_url)
			writePage(img_url, j, path)
			j += 1
		print("----finished%d----"%n)
	else:
		print(path + " :已存在")
	n += 1
	return n

def dealPage(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
	request = urllib.request.Request(url, headers=headers)
	t = random.uniform(0.1, 0.3)
	time.sleep(t)
	response = urllib.request.urlopen(request)
	html = response.read()
	return html

def writePage(link, j, path):
	image = dealPage(link)

	fileName = path + "/" + str(j) + ".jpg"
	if os.path.exists(fileName) == False:
		with open(fileName, "wb") as f:
			f.write(image)

if __name__ == '__main__':
	browser = webdriver.PhantomJS()
	browser.maximize_window()
	i = 1
	n = 1
	latest = int(input("请输入海贼王最新话"))
	while n<=latest:
		url = 'http://ac.qq.com/ComicView/index/id/505430/cid/' + str(i)
		n = loadPage(url, i, n)
		i += 1

	
	browser.quit()