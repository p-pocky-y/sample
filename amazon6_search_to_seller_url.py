# coding:utf-8

from selenium import webdriver
from pandas import *
import csv
import time
import os

os.chdir("/home/ec2-user/environment/sample/")
df = pandas.read_csv('any.csv', index_col=0)

#検索結果ページにアクセス
browser = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")  # DO NOT FORGET to set path
url = "https://www.amazon.co.jp/s/ref=nb_sb_noss_2?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords=%E4%B8%A6%E8%A1%8C%E8%BC%B8%E5%85%A5"
browser.get(url)

#変数定義
list = []
n_url1 = "https://www.amazon.co.jp/gp/offer-listing/"
n_url2 = "/ref=dp_olp_new?ie=UTF8&condition=new"
xpath1 = "//div[@class='a-row a-spacing-mini olpOffer'][position()="
xpath2 = "]//h3/span/a"
s_url1 = "https://www.amazon.co.jp/s?marketplaceID=A1VC38T7YXB528&redirect=true&me="
s_url2 = "&merchant="
page = 1

#検索結果の中から商品のURLを取得する
while True:
    #検索結果のAsin番号をリストにして一時的に保存
    p_asins = browser.find_elements_by_css_selector(".s-result-item.celwidget")
    del list[:]
    for p_asin in p_asins:
        list.append(p_asin.get_attribute("data-asin"))

    for l in list:
        #順番に新品の出品者ページへ遷移
        np_url = n_url1+str(l)+n_url2
        browser.get(np_url)
        browser.implicitly_wait(10)
        print("Moving to next product......")
        print(browser.current_url)
        time.sleep(10)
        position = 1
        
        #出品者のストアフロントへ順番に遷移し、dfにappend
        while True:
            xpath_code = xpath1+str(position)+xpath2
            if len(browser.find_elements_by_xpath(xpath_code))>0:
                p = browser.find_element_by_xpath(xpath_code).get_attribute("href")
                s = p.find('seller')
                seller_id = p[s+7:]
                seller_url = s_url1+seller_id+s_url2+seller_id
                print seller_url
                """se = pandas.Series([seller_url],['seller'])
                df = df.append(se, ignore_index=True)"""
                position+=1
            else:
                print("no seller anymore")
                break

    #次のページがあれば次のページへ遷移
    if len(browser.find_element_by_css_selector(".pagnNextLink")) > 0:
        btn = browser.find_element_by_css_selector(".pagnNextLink").get_attribute("href")
        print("next url:{}".format(btn))
        browser.get(btn)
        page+=1
        browser.implicitly_wait(10)
        print("Moving to next page......")
        time.sleep(10)
    else:
        print("no pager exist anymore")
        break

df.to_csv("seller_url.csv")
print("DONE")
