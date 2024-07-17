# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class BookScraperPipeline:
    def open_spider(self, spider):
        self.file = open('output.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, fields_to_export=[
            'url', 'book_title', 'genre', 'universal_product_code', 'product_type',
            'base_price', 'taxed_price', 'tax', 'stock_count', 'reviews', 'star_rating'
        ])
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        
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
        
        self.exporter.export_item(item)
        return item
