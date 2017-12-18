#get ASIN by seller list csv
#Sample code https://review-of-my-life.blogspot.jp/2017/10/pager-next-selenium.html

from selenium import webdriver
from pandas import *
import csv
import time
import os

#Access to page

browser = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")  # DO NOT FORGET to set path

os.chdir("/home/ec2-user/environment/sample/")
df = pandas.read_csv('any.csv', index_col=0)

#Insert title,date,bookmarks into CSV file

page = 1 #This number shows the number of current page later
product_num = 0

data=[]
with open('urls.csv','rb') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row[0])

for url in data:
    print url
    browser.get(url)
    while True:
        result_num = "#result_"+str(product_num)
        if len (browser.find_elements_by_css_selector(result_num)) >0:
            producturl = browser.find_element_by_css_selector(result_num).get_attribute("data-asin")
            se = pandas.Series([producturl],['url'])
            df = df.append(se, ignore_index=True)
            product_num+=1
    
        elif len(browser.find_elements_by_css_selector("#pagnNextLink")) > 0:
            btn = browser.find_element_by_css_selector("#pagnNextLink").get_attribute("href")
            print("next url:{}".format(btn))
            browser.get(btn)
            page+=1
            browser.implicitly_wait(10)
            print("Moving to next page......")
            time.sleep(10)
    
        else:
            print("no pager exist anymore")
            break
    
df.to_csv("url.csv")
print("DONE")
