import scrapy
import json

class RealtSpider(scrapy.Spider):
    name = "list"
    count = 0

    start_urls = [
        'https://realt.by/sale/flats/',
    ]

    def parse(self, response):
        file = open('results.json', 'w', encoding='utf-16')
        data = {"items": []}

        for item in response.css('div.bd-item > div.title'):
            data["items"].append({"name":item.css('a::text').extract_first()})

        file.write(json.dumps(data, ensure_ascii=False))
        file.close()

        next_page = response.css('div.uni-paging a.active + a::attr("href")').extract_first()
        if next_page is not None and self.count < 10:
            self.count += 1
            yield response.follow(next_page, self.parse)