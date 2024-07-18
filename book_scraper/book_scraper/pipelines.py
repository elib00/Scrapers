# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import mysql.connector


class BookScraperPipeline:
    # def open_spider(self, spider):
    #     self.file = open('output.csv', 'wb')
    #     self.exporter = CsvItemExporter(self.file, fields_to_export=[
    #         'url', 'book_title', 'genre', 'universal_product_code', 'product_type',
    #         'base_price', 'taxed_price', 'tax', 'stock_count', 'reviews', 'star_rating'
    #     ])
    #     self.exporter.start_exporting()
    
    # def close_spider(self, spider):
    #     self.exporter.finish_exporting()
    #     self.file.close()
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        #strip white spaces
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()
        
        #lowercase format
        lowercase_keys = ["genre", "product_type"]
        for key in lowercase_keys:
            value = adapter.get(key)
            adapter[key] = value.lower()
        
        #convert currency to float
        price_keys = ["base_price", "taxed_price", "tax"]
        for key in price_keys:
            value = adapter.get(key)
            value = value.replace("£", "")
            adapter[key] = float(value)
        
        #get the number of stocks for the items
        stock_count_string = adapter.get("stock_count")
        split_string = stock_count_string.split("(")
        
        if len(split_string) < 2:
            adapter["stock_count"] = 0
        else:
            stock_array = split_string[1].split(" ")
            adapter["stock_count"] = int(stock_array[0])
    
        #convert reviews to int
        adapter["reviews"] = int(adapter.get("reviews"))
        
        #get the star rating
        ratings = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
        }
        
        star_rating_string = adapter.get("star_rating")
        stars = star_rating_string.split(" ")[1].lower()
        adapter["star_rating"] = ratings[stars]
        
        # self.exporter.export_item(item)
        return item


class SaveToMySQLPipeline:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = "localhost", user = "root", password = "", database = "db_books"
        )
        
        self.cursor = self.connection.cursor()
        
        query_string = """
            CREATE TABLE IF NOT EXISTS tbl_info (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                url VARCHAR(255),
                book_title VARCHAR(255),
                genre VARCHAR(255),
                universal_product_code VARCHAR(255),
                product_type VARCHAR(255),
                base_price DECIMAL,
                taxed_price DECIMAL,
                tax DECIMAL,
                stock_count INT, 
                reviews INT, 
                star_rating INT   
            ); 
        """
        
        self.cursor.execute(query_string)
        self.connection.commit()
        
    def process_item(self, item, spider):
        query_string = """
            INSERT INTO tbl_info (
                url, book_title, genre, universal_product_code, product_type, base_price,
                taxed_price, tax, stock_count, reviews, star_rating
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        self.cursor.execute(query_string, (
            item["url"], item["book_title"], item["genre"], item["universal_product_code"], item["product_type"],
            item["base_price"], item["taxed_price"], item["tax"], item["stock_count"], item["reviews"], item["star_rating"]
        ))
        
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
            
        
        