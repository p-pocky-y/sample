from selenium import webdriver
from pandas import *
import time
import os

#Access to page

driver = webdriver.PhantomJS()  # DO NOT FORGET to set path
url = "https://www.amazon.co.jp/s/ref=sr_pg_1?me=A1XOU3JTNRE3L1&rh=i%3Amerchant-items&ie=UTF8&qid=1513429349"
driver.get(url)
print(driver)

os.chdir("/home/ec2-user/environment/sample/")
df = pandas.read_csv('any.csv', index_col=0)

#Insert title,date,bookmarks into CSV file

page = 1 #This number shows the number of current page later

print(len(driver.find_elements_by_css_selector("pagnnext")))
