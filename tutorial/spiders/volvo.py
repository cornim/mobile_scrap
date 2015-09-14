'''
Created on Aug 20, 2015

@author: corni
'''

from scrapy import Spider, Request
from tutorial.items import Car
from tutorial.spiders.helper import search_words_yes_no, extract_main_data, plz_dist, block_known_cars
import pickle
import os

class VolvoSpider(Spider):
    name = "volvo"
    allowed_domains = ["mobile.de"]
    start_urls = [
        "http://suchen.mobile.de/auto/search.html?isSearchRequest=true&scopeId=C&makeModelVariant1.makeId=25100&makeModelVariant1.modelId=&makeModelVariant1.modelDescription=&makeModelVariantExclusions[0].makeId=&categories=EstateCar&minSeats=&maxSeats=&doorCount=&minFirstRegistrationDate=2009-01-01&maxFirstRegistrationDate=&minMileage=&maxMileage=150000&minPrice=&maxPrice=24000&minPowerAsArray=150&maxPowerAsArray=&maxPowerAsArray=PS&minPowerAsArray=PS&fuels=DIESEL&transmissions=AUTOMATIC_GEAR&minCubicCapacity=&maxCubicCapacity=&ambitCountry=DE&zipcode=&q=&climatisation=&airbag=&daysAfterCreation=&adLimitation=&export=&vatable=&maxConsumptionCombined=&emissionClass=&emissionsSticker=&damageUnrepaired=NO_DAMAGE_UNREPAIRED&numberOfPreviousOwners=&minHu=&usedCarSeals="
    ]
    
    def __init__(self):
        if os.path.isfile(self.fname):
            with open(self.fname, 'r') as f:
                self.block_list = pickle.load(f)
        
    def save_block_list(self):
        with open(self.fname, 'w') as f:
            pickle.dump(self.block_list, f)        
    
    #List with blocked ad ids
    block_list = []
    fname = "volvo_blocked_ids"

    def parse(self, response):
        for sel in response.xpath("//a[contains(@href,'pageNumber')]"):
            relurl = sel.xpath('@href').extract()
            if len(relurl) == 1:
                relurl = relurl[0]
                url = response.urljoin(relurl)
                if block_known_cars(url, self.block_list):
                    continue
        
                #print url
                if "search.html" in url:
                    yield Request(url, callback=self.parse)
                if "details.html" in url:
                    yield Request(url, callback=self.parse_car)
    
            
    def parse_car(self, response):
        data = response.xpath("//div[@id='ad-description']").extract()
        if len(data)==1:
            data = data[0].lower()
            check1 = ("aktive geschw", "adaptive cruise control", "abstandsregelung",  "abstandregelung"
                      "driving assistant plus", "fahrerassistenz-paket", "fahrerassistenz paket",
                      "fahrassistenz-paket", "fahrassistenz paket", "abstandsregeltempomat")
            if any(word in data for word in check1):
                ret = Car()
                
                extract_main_data(response, ret)
                
                search_words_yes_no(["komfortzugang", "keyless"], data, ret, 'keyless')
                search_words_yes_no(["adaptive drive"], data, ret, 'adaptive_drive')
                search_words_yes_no(["driving assistant plus", "stauassistent"], data, ret, 'stau_assi')
                search_words_yes_no(["rtti", "traffic information"], data, ret, 'RTTI')
                ret['m_paket'] = "N"
                
                ret['dist'] = plz_dist(response, "60314")
                
                ret['price'] = response.xpath("//p[contains(@class, 'pricePrimaryCountryOfSale priceGross')]/text()").extract()[0]
                ret['url'] = response.url
                yield ret


                
                
                
        #connectedDrive
        #adaptive drive
        #Keyless Drive / Keyless Vehicle
        #fahrerassistenz