#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  

import os
from selenium import webdriver

def FireFox():
	FFBrowser = 'D:/Program Files/Mozilla Firefox'
	driver = webdriver.Firefox(FFBrowser)
	return(driver)

def Chrome():
	ChomeBrowser ='C:/Program Files (x86)/Google/Chrome/Application'
	driver = webdriver.Chrome(ChomeBrowser)
	return(driver)