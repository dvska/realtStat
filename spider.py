import scrapy
import json
import html
import re
import matplotlib.pyplot as plt
import pandas as pd
from pandas.io.json import json_normalize


class RealtSpider(scrapy.Spider):
    name = "list"
    count = 0
    data = {"items": []}

    start_urls = [
        'https://realt.by/sale/flats/',
    ]

    def parse(self, response):
        items = response.css('div.bd-item')

        for item in items:
            price = re.findall('(\d+\s*\d*)', html.unescape(item.css('span.price-byr::text').extract_first()))
            if len(price) > 0:
                price = float(re.sub(r"\s+", "", price[0]))
            else:
                price = None
            name = item.css('div.title a::text').extract_first()
            self.data["items"].append({"name": name, "price": price})

        next_page = response.css('div.uni-paging a.active + a::attr("href")').extract_first()
        if next_page is not None and self.count < 10:
            self.count += 1
            yield response.follow(next_page, self.parse)
        else:
            self.data["count"] = len(self.data["items"])
            file = open('results.json', 'w', encoding='utf-16')
            file.write(json.dumps(self.data, ensure_ascii=False, indent=4))
            file.close()

            df = json_normalize(self.data['items'])
            df.price = df.price.apply(pd.to_numeric)

            mi = df.price.min()
            ma = df.price.max()

            intervalcount = 6

            delta = int((ma - mi) / intervalcount)

            intervals = []

            for i in range(0, intervalcount - 1):
                intervals.append((mi - 1, mi + delta))
                mi += delta

            intervals.append((mi - 1, ma))

            results = []
            for i in intervals:
                results.append(len(df[(df.price > i[0]) & (df.price <= i[1])]))

            x = range(0, 6)
            labels = ['{} to {}'.format(x[0], x[1]) for x in intervals]

            plt.plot(x, results, 'ro')
            plt.xticks(x, labels, rotation='vertical')
            plt.margins(0.2)
            plt.show()