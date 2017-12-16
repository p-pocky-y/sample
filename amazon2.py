from selenium import webdriver
from pandas import *
import time
import os

#Access to page

browser = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")  # DO NOT FORGET to set path
url = "https://www.amazon.co.jp/Vicks-V150SGN-VICKS-%E3%82%B9%E3%83%81%E3%83%BC%E3%83%A0%E5%BC%8F%E5%8A%A0%E6%B9%BF%E5%99%A8-V150SGN-%E4%B8%A6%E8%A1%8C%E8%BC%B8%E5%85%A5%E5%93%81/dp/B017PUA2HS/ref=sr_1_2?m=A1XOU3JTNRE3L1&s=merchant-items&ie=UTF8&qid=1513433839&sr=1-2"
browser.get(url)

os.chdir("/home/ec2-user/environment/sample/")
df = pandas.read_csv('any.csv', index_col=0)

#Insert title,date,bookmarks into CSV file

page = 1 #This number shows the number of current page later

print(browser.find_element_by_xpath("//*[@id='prodDetails']/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]").text)

