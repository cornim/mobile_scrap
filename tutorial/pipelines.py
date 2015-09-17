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
                    base_price = 60000
                if spider.name == "volvo":
                    base_price = 55000
                acc_age = (2016-int(item['ez']) + int(item['km'])/25000.0)
                base_price = base_price * math.exp(-0.12*acc_age)
                base_price = base_price - int(item['dist'])*2
                
                base_price = self.mod_price(base_price, item['keyless'], 3000)
                base_price = self.mod_price(base_price, item['navi_prof'], 3000)
                base_price = self.mod_price(base_price, item['HUD'], 2000)
                base_price = self.mod_price(base_price, item['adap_drive'], 2000)
                base_price = self.mod_price(base_price, item['ddc'], 1800)
                base_price = self.mod_price(base_price, item['m_paket'], 1500)
                base_price = self.mod_price(base_price, item['act_ilenk'], 1200)
                base_price = self.mod_price(base_price, item['p_assi'], 1200)
                base_price = self.mod_price(base_price, item['komf_sitz'], 1000)
                base_price = self.mod_price(base_price, item['speed_l_i'], 800)
                base_price = self.mod_price(base_price, item['fl_assi'], 700)
                base_price = self.mod_price(base_price, item['s_view'], 600)
                base_price = self.mod_price(base_price, item['adapt_kl'], 500)
                base_price = self.mod_price(base_price, item['ah_kupp'], 500)
                base_price = self.mod_price(base_price, item['sw_warn'], 400)
                base_price = self.mod_price(base_price, item['sc_auto'], 250)
                base_price = self.mod_price(base_price, item['gt_oeff'], 150)
                base_price = self.mod_price(base_price, item['auto_h_k'], 150)
                base_price = self.mod_price(base_price, item['r_cam'], 100)
                base_price = self.mod_price(base_price, item['act_lenk'], 0)
                
                #Never present
                base_price = self.mod_price(base_price, item['stau_assi'], 5000)
                base_price = self.mod_price(base_price, item['RTTI'], 2500)
                base_price = self.mod_price(base_price, item['act_sitz'], 800)
                
                item['price_calc'] = round(base_price)
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
                              "keyless", "navi_prof", "HUD", "adap_drive", "ddc", "m_paket", "act_ilenk",
                              "p_assi", "komf_sitz","speed_l_i", "fl_assi","s_view","adapt_kl","ah_kupp",
                              "sw_warn","sc_auto","gt_oeff",
                              "auto_h_k","r_cam","act_lenk",
                              "act_sitz","stau_assi", "RTTI",
                              "url"]
                writer = csv.DictWriter(f, fieldnames)
                writer.writeheader()
                for item in items_sorted:
                    writer.writerow(dict(item.items()))
