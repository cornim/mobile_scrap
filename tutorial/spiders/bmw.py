'''
Created on Aug 20, 2015

@author: corni
'''

from scrapy import Spider, Request
from tutorial.items import Car
from tutorial.spiders.helper import search_words_yes_no, extract_main_data, plz_dist

class BmwSpider(Spider):
    name = "bmw"
    allowed_domains = ["mobile.de"]
    start_urls = [
        "http://suchen.mobile.de/auto/search.html?isSearchRequest=true&sortOption.sortBy=searchNetGrossPrice&fuels=DIESEL&sortOption.sortOrder=ASCENDING&features=HEAD_UP_DISPLAY&damageUnrepaired=NO_DAMAGE_UNREPAIRED&ambitCountry=DE&scopeId=C&transmissions=AUTOMATIC_GEAR&categories=EstateCar&maxMileage=150000&minPowerAsArray=150&minPowerAsArray=KW&minFirstRegistrationDate=2011-01-01&maxPrice=310000&makeModelVariant1.makeId=3500&makeModelVariant1.modelId=16%2C17%2C74%2C18%2C19%2C20%2C21%2C22%2C65%2C23%2C66%2C24%2C25%2C26%2C67%2C70&makeModelVariant1.modelGroupId=22"
    ]
    
    #List with blocked ad ids
    block_list = ["211636058"]

    def parse(self, response):
        for sel in response.xpath("//a[contains(@href,'pageNumber')]"):
            relurl = sel.xpath('@href').extract()
            if len(relurl) == 1:
                relurl = relurl[0]
                url = response.urljoin(relurl)
                #print url
                if "search.html" in url:
                    yield Request(url, callback=self.parse)
                if "details.html" in url:
                    yield Request(url, callback=self.parse_car)
    
            
    def parse_car(self, response):
        data = response.xpath("//div[@id='ad-description']").extract()
        if len(data)==1:
            data = data[0].lower()
            check1 = ("aktive geschw", "adaptive cruise control", "acc", "abstandsregelung", "driving assistant plus")
            if True or any(word in data for word in check1) \
            and not any(ad_id in response.url for ad_id in self.block_list):
                ret = Car()
                
                extract_main_data(response, ret)
                
                search_words_yes_no(["komfortzugang", "keyless"], data, ret, 'keyless')
                search_words_yes_no(["adaptive drive"], data, ret, 'adaptive_drive')
                search_words_yes_no(["driving assistant plus", "stauassistent"], data, ret, 'stau_assi')
                search_words_yes_no(["rtti", "traffic information"], data, ret, 'RTTI')
                search_words_yes_no(['aerodynamikpaket', 'aerodynamik-paket', 'aerodynamik paket',
                                     'sportpaket', 'sport-paket', 'sport paket',
                                     'm-paket', 'm paket'], data, ret, 'm_paket')
                
                ret['dist'] = plz_dist(response, "60314")

                ret['price'] = response.xpath("//p[contains(@class, 'pricePrimaryCountryOfSale priceGross')]/text()").extract()[0]
                ret['url'] = response.url
                yield ret
                

                
                
                
        #connectedDrive
        #adaptive drive
        #Keyless Drive / Keyless Vehicle
        #fahrerassistenz