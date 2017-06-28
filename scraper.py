import scrapy
from scrapy.crawler import CrawlerProcess
from spider import RealtSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'FEED_URI': 'result.json'
})

process.crawl(RealtSpider)
process.start()