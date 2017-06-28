import scrapy


class RealtSpider(scrapy.Spider):
    name = "list"
    start_urls = [
        'https://realt.by/sale/flats/',
    ]

    def parse(self, response):
        filename = 'results.txt'

        with open(filename, 'wb') as f:
            for item in response.css('div.bd-item > div.title'):
                f.write(item.css('a::text').extract_first())

        next_page = response.css('div.uni-paging a.active + a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)