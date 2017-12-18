#get ASIN by indivisual product page

from selenium import webdriver
from pandas import *
import time
import os

#Access to page

browser = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")  # DO NOT FORGET to set path
url = "https://www.amazon.co.jp/%E3%83%9E%E3%83%A4%E3%83%88%E3%82%A4%E3%82%BA-Orbeez-Treats-Studio-47350/dp/B00X9ZPZFI/ref=sr_1_1?m=A1XOU3JTNRE3L1&s=merchant-items&ie=UTF8&qid=1513437079&sr=1-1"
browser.get(url)

os.chdir("/home/ec2-user/environment/sample/")
df = pandas.read_csv('any.csv', index_col=0)

#Insert title,date,bookmarks into CSV file

page = 1 #This number shows the number of current page later

print(browser.find_element_by_name("ASIN").get_attribute("value"))

