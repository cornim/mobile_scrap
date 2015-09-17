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
                    base_price = 70000
                if spider.name == "volvo":
                    base_price = 55000
                acc_age = (2016-int(item['ez']) + int(item['km'])/25000.0)
                base_price = base_price * math.exp(-0.12*acc_age)
                base_price = base_price - int(item['dist'])*2
                
                base_price = self.mod_price(base_price, item['keyless'], 1000)                
                base_price = self.mod_price(base_price, item['m_paket'], 2000)
                base_price = self.mod_price(base_price, item['komf_sitz'], 600)
                base_price = self.mod_price(base_price, item['act_sitz'], 500)
                base_price = self.mod_price(base_price, item['sc_auto'], 250)
                base_price = self.mod_price(base_price, item['gt_oeff'], 150)
                base_price = self.mod_price(base_price, item['ah_kupp'], 500)
                
                base_price = self.mod_price(base_price, item['adap_drive'], 2500)
                base_price = self.mod_price(base_price, item['stau_assi'], 5000)
                base_price = self.mod_price(base_price, item['auto_h_k'], 250)
                base_price = self.mod_price(base_price, item['fl_assi'], 700)
                base_price = self.mod_price(base_price, item['adapt_kl'], 300)
                base_price = self.mod_price(base_price, item['act_lenk'], 0)
                base_price = self.mod_price(base_price, item['act_ilenk'], 500)
                
                base_price = self.mod_price(base_price, item['RTTI'], 1500)
                base_price = self.mod_price(base_price, item['navi_prof'], 1000)
                base_price = self.mod_price(base_price, item['speed_l_i'], 300)
                base_price = self.mod_price(base_price, item['sw_warn'], 250)
                
                base_price = self.mod_price(base_price, item['r_cam'], 100)
                base_price = self.mod_price(base_price, item['s_view'], 100)
                base_price = self.mod_price(base_price, item['p_assi'], 500)
                
                item['price_calc'] = base_price
                item['price_diff'] = item['price_calc'] - item['price']
        
        if spider.write_csv:
            self.items.append(item)
        
        #if item['price_diff'] >= 0:
        if spider.send_mail:
            self.send_mail(spider, item)            
        
        return item
    
    def mod_price(self, price, feature, value):
        if feature == 'Y':
            return (price + value)
        else:
            return price
    
    def send_mail(self, spider, item):
        if spider.send_mail:
            subject = spider.name + ": Price diff = " + str(item['price_diff'])
            text = '\n\n'.join(str(key)+"="+str(val) for (key,val) in dict(item.items()).items())
            self.email.send_mail(text, subject)
    
    def open_spider(self, spider):
        if spider.send_mail:
            self.email.start_server()
    
    def close_spider(self, spider):
        spider.save_block_list()
        if spider.send_mail:
            self.email.stop_server()
        
        if spider.write_csv:
            items_sorted = sorted(self.items, key=lambda x: -x['price_diff'])
            for item in items_sorted:
                for key in item:
                    if isinstance(item[key], unicode):
                        item[key] = item[key].encode('utf-8')
            with open(spider.name + ".csv", 'w') as f:
                fieldnames = ["price", "price_calc", "price_diff", "dist", "ez", "km", "ps", "color_o", "color_i", 
                              "keyless", "m_paket","komf_sitz","act_sitz","ah_kupp","sc_auto","gt_oeff",
                              "adap_drive", "stau_assi","fl_assi","act_ilenk","auto_h_k","adapt_kl","act_lenk",
                              "RTTI","navi_prof","p_assi","speed_l_i","sw_warn","r_cam","s_view",
                              "url"]
                writer = csv.DictWriter(f, fieldnames)
                writer.writeheader()
                for item in items_sorted:
                    writer.writerow(dict(item.items()))
