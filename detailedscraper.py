import html
import re
import scrapy


class DetailedSpider(scrapy.Spider):
    name = "list"
    count = 0
    pages = 1

    start_urls = [
        'https://realt.by/sale/flats/',
    ]

    def parsedetailed(self, response):
        price = re.findall('(\d+\s*\d*)', html.unescape(response.css('span.price-byr::text').extract_first()))
        if len(price) > 0:
            price = float(re.sub(r"\s+", "", price[0]))
        else:
            price = None
        city = response.xpath(
            u'//table/tbody/tr/td[text()="Населенный пункт"]/following-sibling::td/a/strong/text()').extract_first()
        urlparts = response.url.strip("/").split("/")
        return {'city': city, 'price': price, 'id': int(urlparts[len(urlparts)-1])}

    def parse(self, response):
        links = response.css('div.bd-item .title a')

        for link in links:
            yield scrapy.Request(link.css('::attr("href")').extract_first(), self.parsedetailed)

        next_page = response.css('div.uni-paging a.active + a::attr("href")').extract_first()

        if next_page is not None and self.count < self.pages:
            self.count += 1
            yield response.follow(next_page, self.parse)