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
            if item['ez'] and item['km']:
                base_price = 50000 - 2500 * (2016-int(item['ez']) + int(item['km'])/25000.0)
                base_price = self.mod_price(base_price, item['keyless'], 1200)
                base_price = self.mod_price(base_price, item['adaptive_drive'], 1500)
                base_price = self.mod_price(base_price, item['stau_assi'], 4000)
                base_price = self.mod_price(base_price, item['RTTI'], 1000)
                base_price = self.mod_price(base_price, item['m_paket'], 1000)
                base_price = base_price - int(item['dist'])
                item['price_calc'] = base_price
                item['price_diff'] = item['price_calc'] - item['price']
        
            
        self.items.append(item)
        
        return item
    
    def mod_price(self, price, feature, value):
        if feature == 'Y':
            return (price + value)
        else:
            return price
    
    def close_spider(self, spider):
        items_sorted = sorted(self.items, key=lambda x: -x['price_diff'])
        with open(spider.name + ".csv", 'w') as f:
            fieldnames = ["price", "keyless", "adaptive_drive", "m_paket", "stau_assi",
                          "RTTI", "dist", "ez", "km", "ps", "price_calc", "price_diff", "url"]
            writer = csv.DictWriter(f, fieldnames)
            writer.writeheader()
            for item in items_sorted:
                writer.writerow(dict(item.items()))
