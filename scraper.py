from scrapy.crawler import CrawlerProcess

from spider import RealtSpider
from detailedscraper import DetailedSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(DetailedSpider)
process.start()




