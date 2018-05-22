# !/usr/bin/env python3
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
from lxml import etree
import random
import os
import sys
import time 
import json

def get_comic_info():
	# 将漫画目录写入json文件，包括每一章的标题与链接
	url = 'http://ac.qq.com/Comic/comicInfo/id/505430'
	browser.get(url)
	time.sleep(1)
	title_list = browser.find_elements_by_xpath('//div[@id="chapter"]/div/ol[@class="chapter-page-all works-chapter-list"]/li/p/span/a')
	comic_info = []
	for content in title_list:
		name = content.get_attribute('title')
		link = content.get_attribute('href')
		info_dict = {name:link}
		comic_info.append(info_dict)
	return comic_info

def write_info(file_name, info):
	for i in info:
		# 只有这样处理编码才能在json中显示中文
		# 目前还不知道有什么更好的解决方法
		i = json.dumps(i, ensure_ascii=False).encode()
		with open(file_name, "ab") as f:
			f.write(i + b'\n')

def read_info(file_name):
	read_list = []
	with open(file_name, 'rb') as f:
		saved_file = f.readline().decode()
		while saved_file:
			read_list.append(saved_file)
			saved_file = f.readline().decode()
	return read_list

def deal_image(url):
	# 处理图片链接
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
	request = urllib.request.Request(url, headers=headers)
	# t = random.uniform(0.1, 0.3)
	# time.sleep(t)
	response = urllib.request.urlopen(request)
	html = response.read()
	return html

def write_image(url, j, path):
	image = deal_image(url)
	fileName = path + "/" + str(j) + ".jpg"
	if os.path.exists(fileName) == False:
		with open(fileName, "wb") as f:
			f.write(image)

def loadPage(url, name):
	browser.get(url)
	# 先找到一幅未加载漫画的图片位置
	targets = browser.find_elements_by_xpath('//div/ul/li[@style]/img[@src="//ac.gtimg.com/media/images/pixel.gif"]')
	target = targets[0]
	while target:
		# 不断跳转到未加载图片位置，让漫画加载出来
		browser.execute_script("arguments[0].scrollIntoView();", target)
		targets = browser.find_elements_by_xpath('//div/ul/li[@style]/img[@src="//ac.gtimg.com/media/images/pixel.gif"]')
		# 判断是否全部加载完毕
		if len(targets) == 0:
			break
		target = targets[0]
	comicLinks = browser.find_elements_by_xpath('//div/ul/li[@style]/img')
	j = 1 
	path ="./Comic/" + name[4:]
	try:
		os.makedirs(path)
	except:
		path = "./Comic/" + name[4:9]
		os.makedirs(path)
	for element in comicLinks:
		img_url = element.get_attribute('src')
		write_image(img_url, j, path)
		j += 1
	print("----%s：已下载完毕----"%name[4:])
	
if __name__ == '__main__':
	# browser = webdriver.PhantomJS()
	browser = webdriver.Chrome()
	file_name = './Comic/comic-info.json'
	# 判断是否已经有存好信息的json文件
	# 如果没有就获取漫画目录信息写入json文件
	if os.path.exists(file_name) == False:
		info = get_comic_info()
		write_info(file_name, info)
	# 否则读取json文件，开始准备下载漫画
	# 计数，统计已下载的漫画数
	count = -1
	for fn in os.listdir("./Comic"): #fn 表示的是文件名
		count = count+1
	print("开始下载漫画")
	read_list = read_info(file_name)
	latest = int(input("请输入海贼王最新话"))
	while count<latest:
		now_file = eval(read_list[count])
		name = list(now_file.keys())[0]
		link = list(now_file.values())[0]
		loadPage(link, name)
		count += 1

	browser.quit()