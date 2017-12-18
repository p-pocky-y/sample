# coding:utf-8

from selenium import webdriver
from pandas import *
import csv
import time
import os

os.chdir("/home/ec2-user/environment/sample/")
df = pandas.read_csv('any.csv', index_col=0)

browser = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")  # DO NOT FORGET to set path
url = "https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords=%E4%B8%A6%E8%A1%8C%E8%BC%B8%E5%85%A5&rh=i%3Aaps%2Ck%3A%E4%B8%A6%E8%A1%8C%E8%BC%B8%E5%85%A5"
xpath1 = "//div[@class='a-row a-spacing-mini olpOffer'][position()="
xpath2 = "]//h3/span/a"
s_url1 = "https://www.amazon.co.jp/s?marketplaceID=A1VC38T7YXB528&redirect=true&me="
s_url2 = "&merchant="
position = 1
page = 1

browser.get(url)
p_asin = browser.find_elements_by_css_selector(".s-result-item.celwidget")
b=[]
for p_url in p_asin:
    b.append(p_url.get_attribute("data-asin"))

for a in b:
    print(a)
    
    
