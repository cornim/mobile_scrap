# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

#from scrapy.exceptions import DropItem
import re
import csv
from tutorial.send_gmail import GmailSender
import math

class CarPipeline(object):
    
    items = list()
    email = GmailSender()
    
    def process_item(self, item, spider):
        if item['price']:
            digits = re.findall(r'\d+', item['price'])
            item['price'] = int("".join(digits))
            if item['ez'] and item['km']:
                base_price = 0
                if spider.name == 'bmw':
                    base_price = 80000
                if spider.name == "volvo":
                    base_price = 55000
                acc_age = (2016-int(item['ez']) + int(item['km'])/25000.0)
                base_price = base_price * math.exp(-0.12*acc_age)
                base_price = self.mod_price(base_price, item['keyless'], 1500)
                base_price = self.mod_price(base_price, item['adaptive_drive'], 2500)
                base_price = self.mod_price(base_price, item['stau_assi'], 5000)
                base_price = self.mod_price(base_price, item['RTTI'], 1500)
                base_price = self.mod_price(base_price, item['m_paket'], 1500)
                base_price = base_price - int(item['dist'])*2
                item['price_calc'] = base_price
                item['price_diff'] = item['price_calc'] - item['price']
        
        self.items.append(item)
        
        #if item['price_diff'] >= 0:
        self.send_mail(spider, item)            
        
        return item
    
    def mod_price(self, price, feature, value):
        if feature == 'Y':
            return (price + value)
        else:
            return price
    
    def send_mail(self, spider, item):
        subject = spider.name + ": Price diff = " + str(item['price_diff'])
        text = '\n\n'.join(str(key)+"="+str(val) for (key,val) in dict(item.items()).items())
        self.email.send_mail(text, subject)
    
    def open_spider(self, spider):
        self.email.start_server()
    
    def close_spider(self, spider):
        spider.save_block_list()
        self.email.stop_server()
        
        items_sorted = sorted(self.items, key=lambda x: -x['price_diff'])
        with open(spider.name + ".csv", 'w') as f:
            fieldnames = ["price", "keyless", "adaptive_drive", "m_paket", "stau_assi",
                          "RTTI", "dist", "ez", "km", "ps", "price_calc", "price_diff", "url"]
            writer = csv.DictWriter(f, fieldnames)
            writer.writeheader()
            for item in items_sorted:
                writer.writerow(dict(item.items()))
