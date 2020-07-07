from scrapy import Spider, Request
from ynab.items import YnabItem
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import datetime
import re

class YnabSpider(Spider):
  name = 'ynab_spider'
  allowed_urls = ['https://support.youneedabudget.com/']
  start_urls = ['https://support.youneedabudget.com/topics?sort=no_sort']

  def parse(self, response):
    page_count = int(response.xpath('//div[@id="pageNav"]/a[5]/text()').extract_first())

    page_urls = ['https://support.youneedabudget.com/topics?pg={}&sort=no_sort'.format(x) for x in range(1,page_count)]

    for url in page_urls:
      yield Request(url=url, callback=self.parse_posts_list)

  def parse_posts_list(self, response):
    post_urls = response.xpath('//a[@class="topic-summary__text-link -topic"]/@href').extract()
    for url in ['https://support.youneedabudget.com{}'.format(x) for x in post_urls]:
        yield Request(url=url, callback=self.parse_post_page)

  def parse_post_page(self, response):
    
    def parse_post_info():
      options = webdriver.ChromeOptions()
      options.add_argument("headless")
      driver = webdriver.Chrome(executable_path = r'C:\Program Files\chromedriver.exe', options=options)
      driver.get(response.url)
      action = ActionChains(driver)
      posted_path = driver.find_element_by_xpath('//span[@class=" said_on infotip screenonly"]')
      action.move_to_element(posted_path).perform()
      time.sleep(1)
      posted_details = driver.find_element_by_xpath('//span[@class="infodate__created"]').text
      return datetime.datetime.strptime(posted_details, '%b %d, %Y · %H:%M %p')

    posted = parse_post_info()
    
    category = response.xpath('//a[@class="site-breadcrumb__link -category"][2]/text()').extract_first()

    title = response.xpath('//h1[@class="topic__title"]/text()').extract_first()
    
    user = response.xpath('//li[@class="topic-meta__item topic-meta__handle at-handle"]/text()').extract_first()
    
    text = response.xpath('//div[@class="cfa topic__text formatted"]//text()').extract()
    text = ''.join(text)
    text = re.sub('\s+', ' ', text)
    text = text.replace("\"", "")
    text = text.strip()
    
    likes = response.xpath('//div[@class="panel panel-stats"]/ul/li[@class="-divider"]/span[contains(text(),"Likes")]/preceding-sibling::span/text()').extract_first()
    if likes == None:
      likes = 0

    replies = response.xpath('//span[@class="panel__value replyCount"]/text()').extract_first()
    if replies == None:
      replies = 0

    views = response.xpath('//div[@class="panel panel-stats"]/ul/li[@class="-divider"]/span[contains(text(),"Views")]/preceding-sibling::span/text()').extract_first()
    
    following = response.xpath('//li[@id="followingItem"]/span[1]/text()').extract_first()
    if following == None:
      following = 0

    item = YnabItem()
    item["category"] = category
    item["title"] = title
    item["user"] = user
    item["posted"] = posted
    item["text"] = text
    item["replies"] = replies
    item["likes"] = likes
    item["views"] = views
    item["following"] = following
    yield item