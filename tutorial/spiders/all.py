'''
Created on Aug 20, 2015

@author: corni
'''

from scrapy import Spider, Request
import os
import pickle
import re
import logging
import pygeodb

class CarSpider(Spider):
    
    send_mail = False
    write_csv = True
    use_block_list = False
    
    def __init__(self, *args, **kwargs):
        self.process_kwargs(kwargs)
        self.load_block_list()
        super(CarSpider, self).__init__(*args, **kwargs)
    
    def process_kwargs(self, kwargs):
        send_mail = "send_mail"
        if send_mail in kwargs:
            if kwargs[send_mail] != "0" and kwargs[send_mail].lower() != "false":
                self.send_mail = True
            else:
                self.send_mail = False
            del kwargs[send_mail]
            
        write_csv = "write_csv"
        if write_csv in kwargs:
            if kwargs[write_csv] != "0" and kwargs[write_csv].lower() != "false":
                self.write_csv = True
            else:
                self.write_csv = False
            del kwargs[write_csv]
            
        use_block_list = "use_block_list"
        if use_block_list in kwargs:
            if kwargs[use_block_list] != "0" and kwargs[use_block_list].lower() != "false":
                self.use_block_list = True
            else:
                self.use_block_list = False
            del kwargs[use_block_list]
    
    def load_block_list(self):
        if self.use_block_list and os.path.isfile(self.fname):
            with open(self.fname, 'r') as f:
                self.block_list = pickle.load(f)
                
    def save_block_list(self):
        if self.use_block_list:
            with open(self.fname, 'w') as f:
                pickle.dump(self.block_list, f)
        
    block_list = []

    def parse(self, response):
        for sel in response.xpath("//a[contains(@href,'pageNumber')]"):
            relurl = sel.xpath('@href').extract()
            if len(relurl) == 1:
                relurl = relurl[0]
                url = response.urljoin(relurl)
                if self.block_known_cars(url, self.block_list):
                    continue
                
                #print url
                if "search.html" in url:
                    yield Request(url, callback=self.parse)
                if "details.html" in url:
                    yield Request(url, callback=self.parse_car)
                    
    def search_words_yes_no(self, words, data, car_item, car_field):
        if any(word in data for word in words):
            car_item[car_field] = "Y"
        else:
            car_item[car_field] = "N"
        
    def extract_main_data(self, response, car_item):
        main_data = "".join(response.xpath("//div[@class='mainTechnicalData']/p/text()").extract())
        try:
            ez_match = re.match(r".*([0-9]{2}).([0-9]{4}).*", main_data, flags=re.DOTALL)
            car_item['ez'] = round(int(ez_match.group(2)) + int(ez_match.group(1))/12.0,1)
        except:
            logging.exception("No ez for url " + response.url)
        
        try:
            km_match = re.match(r".* ([0-9.]+).km", main_data, flags=re.DOTALL)
            car_item['km'] = int(re.sub("\.","",km_match.group(1)))
        except:
            logging.exception("No km for url " + response.url)
        
        try:
            ps_match = re.match(r".*\(([0-9]+).PS", main_data, flags=re.DOTALL)
            car_item['ps'] = int(ps_match.group(1))
        except:
            logging.exception("No ps for url " + response.url)
            
        try:
            car_item['color_o'] = "".join(response.xpath("//dt[text()='Farbe:']/following-sibling::dd[1]/text()").extract())
        except:
            logging.exception("No outside color for url " + response.url)
        try:
            car_item['color_i'] = "".join(response.xpath("//dt[text()='Farbe der Innenausstattung:']/following-sibling::dd[1]/text()").extract())
        except:
            logging.exception("No inside color for url " + response.url)
            
    def plz_dist(self, response, home_plz):
        address_text = "".join(response.xpath("//p[@id='vcardAddress']/text()").extract())
        re_match = re.match(r".*([0-9]{5}).*", address_text, flags=re.DOTALL)
        if re_match:
            car_plz = re_match.group(1)
            dist = pygeodb.distance(home_plz, car_plz)/1000
        else:
            dist = 1000
        return dist
    
    def block_known_cars(self, url, block_list):
        car_id = self.get_id(url)
        if car_id != None:
            if car_id in block_list:
                return True
            else:
                block_list.append(car_id)
                return False
    
    def get_id(self, url):
        re_match = re.match(r".*id=([0-9]+)", url)
        if re_match == None:
            return None
        else:
            return re_match.group(1)