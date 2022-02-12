# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose

def clean_space(value):
    value = value.strip().replace('\xa0', '')
    return value

def clean_float(value):
    try:
        value = float(value)
    except ValueError:
        pass
    return value

class LmparcerItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(input_processor=MapCompose(clean_space), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clean_space, clean_float), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()

