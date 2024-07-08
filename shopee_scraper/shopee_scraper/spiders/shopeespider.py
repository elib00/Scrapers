import scrapy


class ShopeespiderSpider(scrapy.Spider):
    name = "shopeespider"
    allowed_domains = ["shopee.ph"]
    start_urls = ["https://shopee.ph/"]

    def parse(self, response):
        pass
