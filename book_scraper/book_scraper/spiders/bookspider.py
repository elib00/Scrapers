import scrapy
from book_scraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css("article.product_pod")
        
        for book in books:
            book_page_url = book.css("h3 a::attr(href)").get()
            yield response.follow(response.urljoin(book_page_url), callback=self.parse_book_page)
        
        next_page = response.css("li.next a::attr(href)").get()
        
        if next_page:
            yield response.follow(response.urljoin(next_page), callback=self.parse)
        
    def parse_book_page(self, response):
        product_info_container = response.css("table tr")   
        
        book_info = {
            "url": response.url,
            "book_title": response.css("div.product_main h1::text").get(),
            "genre": response.css("ul.breadcrumb li:nth-child(3) a::text").get(),
            "universal_product_code": product_info_container[0].css("td::text").get(),
            "product_type": product_info_container[1].css("td::text").get(),
            "base_price": product_info_container[2].css("td::text").get(),
            "taxed_price": product_info_container[3].css("td::text").get(),
            "tax": product_info_container[4].css("td::text").get(),
            "stock_count": product_info_container[5].css("td::text").get(),
            "reviews": product_info_container[6].css("td::text").get(),
            "star_rating": response.css("p.star-rating::attr(class)").get()
        }
        
        
        book_item = BookItem(**book_info)
        
        yield book_item
