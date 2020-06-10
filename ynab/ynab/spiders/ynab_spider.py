from scrapy import Spider, Request
from ynab.items import YnabItem

class YnabSpider(Spider):
  name = 'ynab_spider'
  allowed_urls = ['https://support.youneedabudget.com/']
  start_urls = ['https://support.youneedabudget.com/topics?sort=no_sort']

  def parse(self, response):
    page_count = int(response.xpath('//div[@id="pageNav"]/a[5]/text()').extract_first())

    page_urls = ['https://support.youneedabudget.com/topics?pg={}&sort=no_sort'.format(x) for x in range(1,page_count)]

    for url in page_urls[:1]:
      yield Request(url=url, callback=self.parse_posts_list)

  def parse_posts_list(self, response):
    post_urls = response.xpath('//a[@class="topic-summary__text-link -topic"]/@href').extract()
    for url in ['https://support.youneedabudget.com{}'.format(x) for x in post_urls]:
        yield Request(url=url, callback=self.parse_post_page)

  def parse_post_page(self, response):
    category = response.xpath('//a[@class="site-breadcrumb__link -category"][2]/text()').extract_first()

    title = response.xpath('//h1[@class="topic__title"]/text()').extract_first()
    
    user = response.xpath('//li[@class="topic-meta__item topic-meta__handle at-handle"]/text()').extract_first()
    
    posted = "" # NEED FROM SELENIUM SCRIPT
    
    text = response.xpath('//div[@class="cfa topic__text formatted"]//text()').extract()
    text = ''.join(text).strip()
    text = text.replace(u'\xa0', '').replace("\"", "").replace(u"\n", " ")

    replies = response.xpath('//span[@class="panel__value replyCount"]/text()').extract_first()
    
    likes = response.xpath('//div[@class="panel panel-stats"]/ul/li[1]/span[1]/text()').extract_first()

    views = response.xpath('//div[@class="panel panel-stats"]/ul/li[4]/span[1]/text()').extract_first()
    
    following = response.xpath('//div[@class="panel panel-stats"]/ul/li[5]/span[1]/text()').extract_first()

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