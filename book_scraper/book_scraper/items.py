# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(scrapy.Item):
    url = scrapy.Field()
    book_title = scrapy.Field()
    genre = scrapy.Field()
    universal_product_code = scrapy.Field()
    product_type = scrapy.Field()
    base_price = scrapy.Field()
    taxed_price = scrapy.Field()
    tax = scrapy.Field()
    stock_count = scrapy.Field()
    reviews = scrapy.Field()
    star_rating = scrapy.Field()