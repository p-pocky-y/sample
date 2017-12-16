#Sample code https://review-of-my-life.blogspot.jp/2017/10/pager-next-selenium.html

from selenium import webdriver
from pandas import *
import time
import os

#Access to page

browser = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")  # DO NOT FORGET to set path
url = "https://www.amazon.co.jp/s/ref=sr_pg_1?me=A1XOU3JTNRE3L1&rh=i%3Amerchant-items&ie=UTF8&qid=1513429349"
browser.get(url)

os.chdir("/home/ec2-user/environment/sample/")
df = pandas.read_csv('any.csv', index_col=0)

#Insert title,date,bookmarks into CSV file

page = 1 #This number shows the number of current page later

while True: #continue until getting the last page
    if len(browser.find_elements_by_css_selector("#pagnNextLink")) > 0:
        print("######################page: {} ########################".format(page))
        print("Starting to get posts...")
        #get all posts in a page
        #maybe no need posts = browser.find_elements_by_css_selector(".search-result")
        goodsurl=browser.find_elements_by_css_selector(".a-link-normal" ".s-access-detail-page" ".s-color-twister-title-link" ".a-text-normal").get_attribute("href")
        se = pandas.Series([url],[goodsurl])
        df = df.append(se, ignore_index=True)
        print(df)
        
        #maybe no need
        """for post in posts:
            title = post.find_element_by_css_selector("h3").text
            date = post.find_element_by_css_selector(".created").text
            bookmarks = post.find_element_by_css_selector(".users span").text
            se = pandas.Series([title, date, bookmarks],['title','date','bookmarks'])
            df = df.append(se, ignore_index=True)
            print(df)"""

        #after getting all posts in a page, click pager next and then get next all posts again
        
        btn = browser.find_element_by_css_selector("#pagnNextLink").get_attribute("href")
        print("next url:{}".format(btn))
        browser.get(btn)
        page+=1
        browser.implicitly_wait(10)
        print("Moving to next page......")
        time.sleep(10)
    else: #if no pager exist, stop.
        print("no pager exist anymore")
        break

df.to_csv("url.csv")
print("DONE")