# coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pandas import *
import csv
import time
import os
import datetime
from selenium.webdriver.chrome.options import Options

browser = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")  # DO NOT FORGET to set path

"""
options = Options()
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
"""

os.chdir("/home/ec2-user/environment/sample/")
df = pandas.read_csv('any.csv', index_col=0)

#モノレートへのリンク用
mono_url1 = "http://mnrate.com/item/aid/"

#Amazonリンク用
ama_jp_url1 = "https://www.amazon.co.jp/exec/obidos/ASIN/"
ama_us_url1 = "https://www.amazon.com/dp/"
ama_ca_url1 = "https://www.amazon.ca/dp/"
ama_uk_url1 = "https://www.amazon.co.uk/dp/"
ama_de_url1 = "https://www.amazon.de/dp/"
ama_fr_url1 = "https://www.amazon.fr/dp/"
ama_it_url1 = "https://www.amazon.it/dp/"
ama_es_url1 = "http://www.amazon.es/dp/"
ama_cn_url1 = "http://www.amazon.cn/dp/"

#国リスト
nation=["us","uk","de","fr","it","es","cn"]

#FBAリンク用
fba_url1 = "https://sellercentral-japan.amazon.com/fba/profitabilitycalculator/index?lang=ja_JP&asin="

#為替レート情報
#http://www.murc-kawasesouba.jp/fx/lastmonth.php
us_rate = 114
ca_rate = 92
uk_rate = 156
de_rate = fr_rate = it_rate = es_rate = 136
cn_rate = 18

#水準
p = 1.2
seller_num = 10
rank_num = 10

#最新のASINリストファイルのNoを記入
now_file = 5
#最新の処理済みが何番目かを記入(出力されてるファイル名を見れば分かる)
now_num = 0

#ASINファイルをリストとして読み込み
data=["B013APQBJU","B0757QKZJK","B013DTCAPC","B01MDS2N5M"]
"""with open("asin_list by" + str(now_file) + "seller.csv",'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row[1])"""

#asinリストの重複を排除して、順番は元の順番を保持する
data = sorted(set(data), key=data.index)

for asin in data[now_num+1:]:
    #モノレートへ遷移
    mono_url = mono_url1 + str(asin)
    #待つ
    browser.get(mono_url)
    browser.implicitly_wait(10)
    print("Moving to mono page......")
    time.sleep(10)
    
    #モノレートから出品者数
    xpath = "//div[@class='list_style_default_parent displayRateComponent']//li[@class='quantity new_price_color _btn_size_style item_conditions_data_box']"
    if len(browser.find_elements_by_xpath(xpath))>0:
        new_sellers = browser.find_element_by_xpath(xpath).text
    else:
        new_sellers = "None"

    #モノレートの日付タブを全て開いてからランキング変動回数を取得
    button = browser.find_elements_by_xpath("//table[@id='sheet_contents']//span[@class='_sheet_accordion_mark original_link _sheet_item_accordion_mark']")
    for c in button:
        c.click()
    count = browser.find_element_by_xpath("//table[@id='sheet_header']//span[@id='ranking_markup_target']").text
    
    #日本の価格を取得
    jp_url = ama_jp_url1 + str(asin)
    #待つ
    browser.get(jp_url)
    browser.implicitly_wait(10)
    print("Moving to amazon page......")
    time.sleep(10)
    if len(browser.find_elements_by_xpath("//span[@id='priceblock_ourprice']"))>0:
        jp = browser.find_element_by_xpath("//span[@id='priceblock_ourprice']").text
    else:
        jp = '1000000000000'
    
    #商品重量を取得
    #ベタ書きパターン
    if len(browser.find_elements_by_xpath("//div[@id='detail_bullets_id']//b[text()='発送重量:']"))>0:
        print(asin)
        pd_text = browser.find_element_by_xpath("//div[@id='detail_bullets_id']//b[text()='発送重量:']/parent::li").text
        weight = pd_text[6:]
    
    #表パターン
    elif len(browser.find_elements_by_xpath("//tr[@class='shipping-weight']/td[@class='value']"))>0:
        weight = browser.find_element_by_xpath("//tr[@class='shipping-weight']/td[@class='value']").text
        
    else:
        weight = "None"
    
    #単位変換
    Kg = weight.find('Kg')
    g = weight.find('g')
    if Kg != -1:
        weight = float(weight[:Kg-1])*1000
    elif g != -1:
        weight = float(weight[:g-1])
    else:
        print(asin+"どげんかせんといかん")
        weight = 0

    postage_ab = weight*1
    postage_dm = weight*0.5
    
    #商品カテゴリ取得
    c
    
    
    #各国の価格取得    
    for n in nation:
        exec("nation_url = ama_%s_url1 + str(asin)" % n) 
        #待つ
        browser.get(nation_url)
        browser.implicitly_wait(10)
        print("Moving to amazon page......")
        time.sleep(10)
        if len(browser.find_elements_by_xpath("//span[@id='priceblock_ourprice']"))>0:
            exec("%s = browser.find_element_by_xpath('''//span[@id='priceblock_ourprice']''').text" % n)
        else:
            exec("%s = '1000000000000'" % n)
    
    #
    for n in nation:
        exec("%s_price_yen = %s*%s_rate" % (n,n,n))

    #手数料計算
    
    
    
    pd_commision = browser.find_element_by_xpath("//div[@id='afn-selling-fees']").text
    fba_commision = browser.find_element_by_xpath("//div[@id='afn-amazon-fulfillment-fees']").text
    
    #利益とイケてる商品判定を追加
    pr = jp_price - postage_ab - postage_dm - pd_commision - fba_commision
    if pr>us_price_yen*p or pr>ca_price_yen*p or pr>uk_price_yen*p or pr>de_price_yen*p or pr>fr_price_yen*p or pr>it_price_yen*p or pr>es_price_yen*p or pr>cn_price_yen*p:
        pr_judge = "◯"
    if new_sellers < seller_num:
        se_judge = "◯"
    if count > rank_num:
        ra_judge = "◯"
    if pr_judge == "◯" and ra_judge == "◯":
        final_judge = "◯"
    
    #今までの情報をpandas上でまとめる
    se = pandas.Series([asin,new_sellers,count,jp_price,us_price_yen,ca_price_yen,uk_price_yen,de_price_yen,fr_price_yen,it_price_yen,es_price_yen,cn_price_yen,weight,postage_ab,postage_dm,pd_commision,fba_commision,pr,pr_judge,se_judge,ra_judge,final_judge],['asin','new_sellers','rankup_count','jp','us','ca','uk','de','fr','it','es','cn','weight','postage_ab','postage_dm','pd_com','fba_com','pr','prj','sej','raj','fij'])
    df = df.append(se, ignore_index=True)
    
    #20asinずつデータとして吐き出す
    l = data.index(asin)
    if l % 3 == 0:
        df.to_csv("pd_research " + str(l) +"asin.csv")
        print("Added pd_research " + str(l) +"asin.csv")
    
df.to_csv("pd_research all " + str(l) + "asin.csv")
print("DONE")
