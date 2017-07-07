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

        trselector = response.xpath(u'//table/tbody/tr')

        city = trselector.xpath(
            u'td[../td[text()="Населенный пункт"]]/a/strong/text()').extract_first()
        district = trselector.xpath(
            u'td[../td[text()="Область"]]/a/text()').extract_first()
        agency = trselector.xpath(
            u'td[text()="Агенство"]').extract_first()
        date = trselector.xpath(
            u'(td[../td[text()="Дата обновления"]])[2]/text()').extract_first()
        street = trselector.xpath(u'td[../td[text()="Адрес"]]/a/text()').extract_first()
        addressline = trselector.xpath(
            u'(td[../td[text()="Адрес"]])[2]/text()').extract_first()
        year = trselector.xpath(
            u'(td[../td[text()="Год постройки"]])[2]/text()').extract_first()

        square = trselector.xpath(
            u'td[../td[contains(text(), "Площадь")]]/strong/text()').extract_first()

        if square is not None:
            squareparts = re.findall('(\d+\.*\d*)', square)
            c = len(squareparts)
            if c > 0:
                obj["square"] = squareparts[0]
            if c > 1:
                obj["livesquare"] = squareparts[1]
            if c > 2:
                obj["kitchensquare"] = squareparts[2]

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
        obj["year"] = year
        return obj

    def parse(self, response):
        links = response.css('div.bd-item .title a')

        for link in links:
            yield scrapy.Request(link.css('::attr("href")').extract_first(), self.parsedetailed)

        next_page = response.css('div.uni-paging a.active + a::attr("href")').extract_first()

        if next_page is not None and self.count < self.pages:
            self.count += 1
            yield response.follow(next_page, self.parse)