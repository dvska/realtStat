from scrapy.crawler import CrawlerProcess
from detailedscraper import DetailedSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 4.0)',
    'ITEM_PIPELINES': {
        'datastoragepipeline.DataStoragePipeline': 100
    }
})

process.crawl(DetailedSpider)
process.start()




