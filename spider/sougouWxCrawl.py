#/usr/bin/python
# coding:utf-8


import time
from lxml import etree
from selenium import webdriver
#from db.MongoHelp import MongoHelper as SqlHelper
from selenium.webdriver import ActionChains

from MongoHelp import MongoHelper as SqlHelper

class WXSpider():
    def __init__(self):
        self.type=['hot','recomment','joke','yangshengtang','shifanghua','baguajing','likelife','finance','auto_moto','technology','fashionbang','hotmother','support','travel','job','delicous','oldToday','study','constellation','sports']
        self.SqlH= SqlHelper()
        self.SqlH.init_db('weixin')
        self.page=2
        self.current_type=''
    def spider(self):
        browser = webdriver.PhantomJS()
        #browser = webdriver.Chrome('/home/caidong/developProgram/selenium/chromedriver')
        for index in range(len(self.type)):
            browser.get('http://weixin.sogou.com/')
            wx.current_type=wx.type[index]
            xpath_str = 'pc_%d' % index
            print(xpath_str)
            if index <= 6:
                bt_element=('//div[@class="fieed-box"]/a[@id="%s"]'%xpath_str)
            else:
                actions = ActionChains(browser)
                more = browser.find_element_by_xpath('//div[@class="fieed-box"]/a[@id="more_anchor"]')
                actions.move_to_element(more).perform()
                bt_element=('//div[@class="tab-box-pop"]/a[@id="%s"]'%xpath_str)
            #if index > 6:
              #  browser.find_element_by_xpath('//div[@class="fieed-box"]/a[@id="pc_6"]').click()
               # time.sleep(2)
            time.sleep(2)
            #actions.move_to_element(more).perform()
            browser.find_element_by_xpath(bt_element).click()
            time.sleep(2)
            #browser.get_screenshot_as_file('tex.png')
            js1 = 'return document.body.scrollHeight'
            js2 = 'window.scrollTo(0, document.body.scrollHeight)'
            old_scroll_height = 0
            while(browser.execute_script(js1) > old_scroll_height):
                old_scroll_height = browser.execute_script(js1)
                browser.execute_script(js2)
                time.sleep(0.8)
            for i in range(self.page):
                load_more_xpath='//div[@class="jzgd"]/a'
                browser.find_element_by_xpath(load_more_xpath).click()
                time.sleep(2)
            html = browser.page_source
            #print(html)
            self.parse(html)
        browser.quit()
    def parse(self,html):
        tree = etree.HTML(html)
        updatetime = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        wx_content = tree.xpath('//ul[@class="news-list"]/li')
        for wx_item in wx_content:
            content = etree.ElementTree(wx_item)
            imgUrl = content.xpath('//img/@src')
            txtTitle = content.xpath('//h3/a/text()')
            detail_url = content.xpath('//h3/a/@href')
            txt_content =  content.xpath('//p/text()')
            print(imgUrl)
            print(txtTitle)
            print(detail_url)
            print(txt_content)
            print('======')
            wxContent = {'title': txtTitle, 'url':detail_url, 'content': txt_content  , 'category': self.current_type,
                               'secCategory': '', 'image':imgUrl , 'time': updatetime, 'from': 'WX'}
            if self.SqlH.count({'title':txtTitle})==0:
                    self.SqlH.insert(wxContent)
        # print(updatetime)
        # imgUrl = '//ul[@class="news-list"]/li/div[@class="img-box"]/a//img/@src'
        # txtTitle = '//ul[@class="news-list"]/li/div[@class="txt-box"]/h3/a/text()'
        # detail_url = '//ul[@class="news-list"]/li/div[@class="txt-box"]/h3/a/@href'
        # txt_content = '//ul[@class="news-list"]/li/div[@class="txt-box"]/p/text()'
        # wx_item_detail_url= tree.xpath(detail_url)
        # wx_item_img_url = tree.xpath(imgUrl)
        # wx_item_text = tree.xpath(txtTitle)
        # wx_item_content = tree.xpath(txt_content)
        # print(len(wx_item_detail_url))
        # print(len(wx_item_img_url))
        # print(len(wx_item_text))
        # print(len(wx_item_content))
        # for i in range(len(wx_item_img_url)):
        #         wxContent = {'title': wx_item_text[i], 'url': wx_item_detail_url[i], 'content':wx_item_content[i] , 'category': self.current_type,
        #                        'secCategory': '', 'image':wx_item_img_url[i] , 'time': updatetime, 'from': 'WX'}
        #         if self.SqlH.count({'title':wx_item_text[i]})==0:
        #             self.SqlH.insert(wxContent)
                    #print(wx_item_content)
                    #print(wx_item_text)
    # for i in range(0,len(news_text)):
    #  if 'http' in news_url[i]:
    #     newsContent  = {'title': news_text[i], 'url': news_url[i], 'content': '', 'category': item,
    #        'secCategory': '', 'image': '', 'time': updatetime, 'from': ''}
    #     count = SqlH.select(1, {'title': news_text[i]})
    #     #print(count)
    #     if len(count) == 0:
    #         SqlH.insert(newsContent)

if __name__ == '__main__':
    #wx = WXSpider()
    while True:
        try:
        #for i in range(20) :
            wx = WXSpider()
            wx.spider()
            #time.sleep(2 * 60 * 60)
        except:
            pass
        time.sleep(2 * 60 * 60)
