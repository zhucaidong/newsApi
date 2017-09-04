#!/usr/bin/env python
# coding:utf-8


import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver import ActionChains
from MongoHelp import MongoHelper as SqlHelper
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import config

class WXSpider():
    def __init__(self):
        self.type=['hot','local','shehui','guonei','guoji','recomment','junshi','finance','technology','sports','fashionbang','fashionbang','auto_moto','fangcan','technology','yangshengtang']
        self.SqlH= SqlHelper()
        self.SqlH.init_db('weixin')
        self.page=2
        self.current_type=''
    def spider(self,inde=None):
        dcap=dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = config.get_header()
        browser = webdriver.PhantomJS(desired_capabilities=dcap)
        #browser = webdriver.Chrome('/home/caidong/developProgram/selenium/chromedriver')
        browser.get('http://news.163.com/')
        #print(browser.page_source)
        for i in range(1,10):
            if i<9:
                bt_mouseover = browser.find_element_by_xpath('//li[@class="nav_item"]['+str(i)+']/a')
                actions =ActionChains(browser)
                actions.move_to_element(bt_mouseover).perform()
                browser.implicitly_wait(5)
                time.sleep(5)
                html = browser.page_source
                #print(html)
                self.current_type=self.type[i]
                self.parse(html)
            else:
                more = browser.find_elements_by_xpath('//div[@class="more_list"]/a')
                i=1
                for item in more:
                    if i < 2:
                        bt_mouseover = browser.find_element_by_xpath('//a[@class="more"]')
                    else:
                        bt_mouseover = browser.find_element_by_xpath('//a[@class="more more_current"]')
                    i += 1
                    actions = ActionChains(browser)
                    actions.move_to_element(bt_mouseover).perform()
                    time.sleep(60)
                    browser.implicitly_wait(50)
                    try:
                        item.click()
                    except:
                        print ("click error")
                    browser.implicitly_wait(15)
                    html = browser.page_source
                    self.current_type = self.type[i+6]
                    print(self.current_type)
                    #print(html)
                    self.parse(html)
                    #actions.click(item)
                    time.sleep(2)

       # browser.get_screenshot_as_file('1.png')
        #print(browser.page_source)
        #exit()
        # if index <= 6:
        #     bt_element=('//div[@class="fieed-box"]/a[@id="%s"]'%xpath_str)
        # else:
        #     actions = ActionChains(browser)
        #     more = browser.find_element_by_xpath('//div[@class="fieed-box"]/a[@id="more_anchor"]')
        #     actions.move_to_element(more).perform()
        #     bt_element=('//div[@class="tab-box-pop"]/a[@id="%s"]'%xpath_str)
        # #if index > 6:
          #  browser.find_element_by_xpath('//div[@class="fieed-box"]/a[@id="pc_6"]').click()
           # time.sleep(2)


        #time.sleep(2)
        #actions.move_to_element(more).perform()
        # browser.find_element_by_xpath(bt_element).click()
        # time.sleep(2)
        #
        # #browser.get_screenshot_as_file('tex.png')
        # js1 = 'return document.body.scrollHeight'
        # js2 = 'window.scrollTo(0, document.body.scrollHeight)'
        # old_scroll_height = 0
        # while(browser.execute_script(js1) > old_scroll_height):
        #     old_scroll_height = browser.execute_script(js1)
        #     browser.execute_script(js2)
        #     time.sleep(0.8)
        # for i in range(self.page):
        #     load_more_xpath='//div[@class="jzgd"]/a'
        #     browser.find_element_by_xpath(load_more_xpath).click()
        #     time.sleep(2)

        browser.quit()
    def parse(self,html):
        tree = etree.HTML(html)
        updatetime = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        news_content = tree.xpath("//div[@class='data_row news_photoview clearfix ']|//div[@class='data_row news_article clearfix ']")
        for item in news_content:
            content = etree.ElementTree(item)
            imgUrl =content.xpath("//img/@src")
            txtTitle = content.xpath("//h3/a/text()")
            detail_url = content.xpath("//h3/a/@href")
            print(imgUrl)
            print(txtTitle)
            print(detail_url)
        wxContent = {'title': txtTitle, 'url': detail_url, 'content': '',
                     'category': self.current_type,
                     'secCategory': '', 'image': imgUrl, 'time': updatetime, 'from': 'WX'}
        if self.SqlH.count({'title': txtTitle}) == 0:
            self.SqlH.insert(wxContent)
        # print(updatetime)
        # imgUrl = '//div[@class="ndi_main"]//img/@src'
        # txtTitle = '//div[@class="ndi_main"]//h3/a/text()'
        # detail_url = '//div[@class="ndi_main"]//h3/a/@href'
        # #txt_content = '//ul[@class="news-list"]/li/div[@class="txt-box"]/p/text()'
        # wx_item_detail_url= tree.xpath(detail_url)
        # wx_item_img_url = tree.xpath(imgUrl)
        # wx_item_text = tree.xpath(txtTitle)
        # #wx_item_content = tree.xpath(txt_content)
        # print(len(wx_item_detail_url))
        # print(len(wx_item_img_url))
        # print(len(wx_item_text))
        # #print(len(wx_item_content))
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
    while True:
        wx = WXSpider()
        wx.spider()
        time.sleep(2 * 60 * 60)