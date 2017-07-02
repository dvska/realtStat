import scrapy
import json
import html
import re


class RealtSpider(scrapy.Spider):
    name = "list"
    count = 0

    start_urls = [
        'https://realt.by/sale/flats/',
    ]

    def parse(self, response):
        file = open('results.json', 'w', encoding='utf-16')
        data = {"items": []}

        for item in response.css('div.bd-item'):
            price = re.findall('(\d+\s*\d*)', html.unescape(item.css('span.price-byr::text').extract_first()))
            if len(price) > 0:
                price = price[0]
            name = item.css('div.title a::text').extract_first()
            data["items"].append({"name": name, "price": price})

        file.write(json.dumps(data, ensure_ascii=False, indent=4))
        file.close()

        next_page = response.css('div.uni-paging a.active + a::attr("href")').extract_first()
        if next_page is not None and self.count < 10:
            self.count += 1
            yield response.follow(next_page, self.parse)