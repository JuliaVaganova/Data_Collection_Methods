import scrapy
from scrapy.http import HtmlResponse
from lmparcer.items import LmparcerItem
from scrapy.loader import ItemLoader


class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/search/?q=газонокосилка']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[@data-qa="product-image"]')
        for link in links:
            yield response.follow(link, callback=self.parse_units)


    def parse_units(self, response: HtmlResponse):
        loader = ItemLoader(item=LmparcerItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photos', "*//img[@alt='product image']/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()



