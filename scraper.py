import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as  np
from operator import attrgetter
from pandas.io.json import json_normalize

from scrapy.crawler import CrawlerProcess
from spider import RealtSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(RealtSpider)
process.start()

file = open('results.json', 'r', encoding='utf-16')
obj = json.load(file)

df = json_normalize(obj['items'])
df.price = df.price.apply(pd.to_numeric)
print(df.price.min())
