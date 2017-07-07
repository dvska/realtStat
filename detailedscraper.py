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
        price = re.findall('(\d+\s*\d*)', html.unescape(response.css('span.price-byr::text').extract_first()))

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

        floor = trselector.xpath(
            u'(td[../td[contains(text(),"Этаж")]])[2]/text()').extract_first()

        ceil = trselector.xpath(
            u'(td[../td[contains(text(),"потолков")]])[2]/text()').extract_first()

        square = trselector.xpath(
            u'td[../td[contains(text(), "Площадь")]]/strong/text()').extract_first()

        obj = self.parsefepage(
            {"price": price, "city": city, "district": district, "agency": agency, "date": date, "street": street,
             "addressline": addressline, "year": year, "floor": floor, "ceil": ceil, "square": square})
        urlparts = response.url.strip("/").split("/")
        obj["id"] = int(urlparts[len(urlparts) - 1])

        return obj


    @staticmethod
    def parsefepage(o):
        obj = {}

        if len(o["price"]) > 0:
            obj["price"] = float(re.sub(r"\s+", "", o["price"][0]))
        else:
            obj["price"] = None

        if o["floor"] is not None:
            floorparts = o["floor"].split('/')
            obj["floor"] = floorparts[0]
            obj["floortotal"] = floorparts[1]

        if o["ceil"] is not None:
            obj["ceil"] = re.findall('(\d+\.*\d*)', o["ceil"])[0]
            obj["ceil"] = re.findall('(\d+\.*\d*)', o["ceil"])[0]

        if o["square"] is not None:
            squareparts = re.findall('(\d+\.*\d*)', o["square"])
            c = len(squareparts)
            if c > 0:
                obj["square"] = squareparts[0]
            if c > 1:
                obj["livesquare"] = squareparts[1]
            if c > 2:
                obj["kitchensquare"] = squareparts[2]

        if o["street"] is not None:
            obj["street"] = o["street"].replace("ул.", "").strip()

        if o["addressline"] is not None:
            addressparts = re.findall('(\d+)', o["addressline"])
            if len(addressparts) > 0:
                obj["house"] = addressparts[0]
            if len(addressparts) > 1:
                obj["flat"] = addressparts[1]

        if o["date"] is not None:
            obj["date"] = datetime.strptime(o["date"], '%Y-%M-%d')

        if o["agency"] is not None:
            obj["agency"] = True
        else:
            obj["agency"] = False

        if o["city"] is not None:
            cityparts = o["city"].split(".")
            obj["city"] = cityparts[len(cityparts) - 1].strip()

        if o["district"] is not None:
            obj["district"] = o["district"].replace("область", "").strip()

        obj["year"] = o["year"]
        return obj


    def parse(self, response):
        links = response.css('div.bd-item .title a')

        for link in links:
            yield scrapy.Request(link.css('::attr("href")').extract_first(), self.parsedetailed)

        next_page = response.css('div.uni-paging a.active + a::attr("href")').extract_first()

        if next_page is not None and self.count < self.pages:
            self.count += 1
            yield response.follow(next_page, self.parse)