# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

#from scrapy.exceptions import DropItem
import re
import csv

class CarPipeline(object):
    
    items = list()
    
    def process_item(self, item, spider):
        if item['price']:
            digits = re.findall(r'\d+', item['price'])
            item['price'] = int("".join(digits))
            
        self.items.append(item)
        
        return item
    
    def close_spider(self, spider):
        items_sorted = sorted(self.items, key=lambda x:x['price'])
        with open(spider.name + ".csv", 'w') as f:
            fieldnames = ["price", "keyless", "adaptive_drive", "stau_assi", "RTTI", "url"]
            writer = csv.DictWriter(f, fieldnames)
            writer.writeheader()
            for item in items_sorted:
                writer.writerow(dict(item.items()))
