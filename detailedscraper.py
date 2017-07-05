import scrapy
import json
import html
import re
import matplotlib.pyplot as plt
import pandas as pd
from pandas.io.json import json_normalize


class DetailedSpider(scrapy.Spider):
    name = "list"
    count = 0
    data = {"items": []}
    pages = 2

    start_urls = [
        'https://realt.by/sale/flats/',
    ]

    def parsedetailed(self, response):
        price = re.findall('(\d+\s*\d*)', html.unescape(response.css('span.price-byr::text').extract_first()))
        if len(price) > 0:
            price = float(re.sub(r"\s+", "", price[0]))
        else:
            price = None
        name = response.css('div.inner-center-content h1::text').extract_first()
        self.data["items"].append({'name': name, 'price': price})
        return self.data

    def parse(self, response):
        links = response.css('div.bd-item .title a')

        for link in links:
            yield scrapy.Request(link.css('::attr("href")').extract_first(), self.parsedetailed)

        next_page = response.css('div.uni-paging a.active + a::attr("href")').extract_first()

        if next_page is not None and self.count < self.pages:
            self.count += 1
            yield response.follow(next_page, self.parse)
        else:
            self.data["count"] = len(self.data["items"])
            file = open('resultsDetailed.json', 'w', encoding='utf-16')
            file.write(json.dumps(self.data, ensure_ascii=False, indent=4))
            file.close()