import scrapy


class RealtSpider(scrapy.Spider):
    name = "list"
    start_urls = [
        'https://realt.by/sale/flats/',
    ]

    def parse(self, response):
        file = open('results.txt', 'w', encoding='utf-16')
        for item in response.css('div.bd-item > div.title'):
            i = item.css('a::text').extract_first()
            file.write(i)
        file.close()


        next_page = response.css('div.uni-paging a.active + a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)