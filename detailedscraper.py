import html
import re
import scrapy
from datetime import datetime


class DetailedSpider(scrapy.Spider):
    name = "list"
    count = 0
    pages = 1

    start_urls = [
        'https://realt.by/sale/flats/',
    ]

    def parsedetailed(self, response):
        obj = {}
        price = re.findall('(\d+\s*\d*)', html.unescape(response.css('span.price-byr::text').extract_first()))

        if len(price) > 0:
            price = float(re.sub(r"\s+", "", price[0]))
        else:
            price = None
        city = response.xpath(
            u'//table/tbody/tr/td[text()="Населенный пункт"]/following-sibling::td/a/strong/text()').extract_first()
        district = response.xpath(
            u'//table/tbody/tr/td[text()="Область"]/following-sibling::td/a/text()').extract_first()
        agency = response.xpath(
            u'//table/tbody/tr/td[text()="Агенство"]').extract_first()
        date = response.xpath(
            u'//table/tbody/tr/td[text()="Дата обновления"]/following-sibling::td/text()').extract_first()
        street = response.xpath(u'//table/tbody/tr/td[text()="Адрес"]/following-sibling::td/a/text()').extract_first()
        addressline = response.xpath(
            u'//table/tbody/tr/td[text()="Адрес"]/following-sibling::td/text()').extract_first()

        if street is not None:
            obj["street"] = street.replace("ул.", "").strip()

        if addressline is not None:
            addressparts = re.findall('(\d+)', addressline)
            if len(addressparts) > 0:
                obj["house"] = addressparts[0]
            if len(addressparts) > 1:
                obj["flat"] = addressparts[1]

        if date is not None:
            date = datetime.strptime(date, '%Y-%M-%d')

        if agency is not None:
            obj["agency"] = True
        else:
            obj["agency"] = False

        if city is not None:
            cityparts = city.split(".")
            city = cityparts[len(cityparts) - 1].strip()

        if district is not None:
            district = district.replace("область", "").strip()

        urlparts = response.url.strip("/").split("/")
        obj["city"] = city
        obj["price"] = price
        obj["id"] = int(urlparts[len(urlparts) - 1])
        obj["district"] = district
        obj["date"] = date
        return obj

    def parse(self, response):
        links = response.css('div.bd-item .title a')

        for link in links:
            yield scrapy.Request(link.css('::attr("href")').extract_first(), self.parsedetailed)

        next_page = response.css('div.uni-paging a.active + a::attr("href")').extract_first()

        if next_page is not None and self.count < self.pages:
            self.count += 1
            yield response.follow(next_page, self.parse)