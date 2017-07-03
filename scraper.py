import json
import pandas as pd
from pandas.io.json import json_normalize

from scrapy.crawler import CrawlerProcess
from spider import RealtSpider
import matplotlib.pyplot as plt

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(RealtSpider)
process.start()




