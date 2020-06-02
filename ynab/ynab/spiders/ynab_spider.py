from scrapy import Spider, Request
from ynab.items import YnabItem

class YnabSpider(Spider):
  name = 'ynab_spider'
  allowed_urls = ['https://support.youneedabudget.com/']
  start_urls = ['https://support.youneedabudget.com/topics?sort=no_sort']

  def parse(self, response):
    # Find the total number of pages in the result so that we can decide how many pages to scrape next
    page_count = int(response.xpath('//div[@id="pageNav"]/a[5]/text()').extract_first())
    # List comprehension to construct all the urls
    page_urls = ['https://support.youneedabudget.com/topics?pg={}&sort=no_sort'.format(x) for x in range(1,page_count)]
    # Yield the requests to different search result urls, 
    # using parse_result_page function to parse the response.
    for url in page_urls:
      yield Request(url=url, callback=self.parse_posts_list)

  def parse_posts_list(self, response):
    post_urls = response.xpath('//a[@class="topic-summary__text-link -topic"]/@href').extract()
    print(len(post_urls))