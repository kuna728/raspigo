from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os, sys
basedir = os.path.abspath(os.path.dirname(__file__))

def DownloadImg(tags=None, constTag='', ratio=16/9, precision=0.03, dir=None):
	display = Display(visible=0, size=(800, 600))
	display.start()
	driver = webdriver.Chrome('/usr/bin/chromedriver')
	driver.maximize_window()
	for tag in tags:
		driver.get('https://images.google.com/')
		try:
			allowBtn = driver.find_element_by_xpath('//*[@id="zV9nZe"]').click()
		except Exception:
			pass
		box = driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
		box.send_keys(tag+constTag)
		box.send_keys(Keys.ENTER)

		i = 1
		last_height = driver.execute_script('return document.body.scrollHeight')
		while True:
			driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
			time.sleep(2)
			new_height = driver.execute_script('return document.body.scrollHeight')
			try:
				while True:
					element = driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[' + str(i) +']/a[1]/div[1]/img')
					h, w = int(element.get_attribute('height')), int(element.get_attribute('width'))
					if abs(w/h - ratio)<=precision:	
						element.click() 
						toDownload = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img')
						url = toDownload.get_attribute("src")
						try:
							os.remove(dir + '/{0}/desktop.png'.format(tag))
						except FileNotFoundError:
							pass
						urllib.request.urlretrieve(url, dir + '/{0}/desktop.png'.format(tag))
						break
					i+=1
				break
			except ZeroDivisionError:
				pass
			last_height = new_height
	driver.quit()

if __name__=="__main__":
	DownloadImg(tags=['Ozark serial'], dir='/home/kuna7/Pulpit/ozark')
