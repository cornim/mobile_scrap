'''
Created on Aug 20, 2015

@author: corni
'''

from scrapy import Spider, Request
from tutorial.items import Car
from tutorial.spiders.helper import search_words_yes_no, extract_main_data, plz_dist

class VolvoSpider(Spider):
    name = "volvo"
    allowed_domains = ["mobile.de"]
    start_urls = [
        "http://suchen.mobile.de/auto/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&scopeId=C&fuels=DIESEL&categories=EstateCar&transmissions=AUTOMATIC_GEAR&maxPrice=25000&minPowerAsArray=110&minPowerAsArray=KW&minFirstRegistrationDate=2009-01-01&maxMileage=150000&makeModelVariant1.makeId=25100&isSearchRequest=true&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING"
    ]
    
    #List with blocked ad ids
    block_list = ["204379153", "208450258"]

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
            check1 = ("aktive geschw", "adaptive cruise control", "abstandsregelung",  "abstandregelung"
                      "driving assistant plus", "fahrerassistenz-paket", "fahrerassistenz paket",
                      "fahrassistenz-paket", "fahrassistenz paket", "abstandsregeltempomat")
            if any(word in data for word in check1) \
            and not any (word in data for word in self.block_list):
                ret = Car()
                
                extract_main_data(response, ret)
                
                search_words_yes_no(["komfortzugang", "keyless"], data, ret, 'keyless')
                search_words_yes_no(["adaptive drive"], data, ret, 'adaptive_drive')
                search_words_yes_no(["driving assistant plus", "stauassistent"], data, ret, 'stau_assi')
                search_words_yes_no(["rtti", "traffic information"], data, ret, 'RTTI')
                
                ret['dist'] = plz_dist(response, "60314")
                
                ret['price'] = response.xpath("//p[contains(@class, 'pricePrimaryCountryOfSale priceGross')]/text()").extract()[0]
                ret['url'] = response.url
                yield ret


                
                
                
        #connectedDrive
        #adaptive drive
        #Keyless Drive / Keyless Vehicle
        #fahrerassistenz