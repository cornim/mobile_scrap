'''
Created on Aug 20, 2015

@author: corni
'''

from scrapy import Spider, Request
from tutorial.items import Car

class BmwSpider(Spider):
    name = "bmw"
    allowed_domains = ["mobile.de"]
    start_urls = [
        "http://suchen.mobile.de/auto/search.html?categories=EstateCar&damageUnrepaired=NO_DAMAGE_UNREPAIRED&features=HEAD_UP_DISPLAY&fuels=DIESEL&transmissions=AUTOMATIC_GEAR&scopeId=C&maxMileage=150000&maxPrice=30000&minPowerAsArray=147&minPowerAsArray=KW&minFirstRegistrationDate=2011-01-01&makeModelVariant1.makeId=3500&makeModelVariant1.modelId=16%2C17%2C74%2C18%2C19%2C20%2C21%2C22%2C65%2C23%2C66%2C24%2C25%2C26%2C67%2C70&makeModelVariant1.modelGroupId=22&isSearchRequest=true&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING"
    ]
    
    #List with blocked ad ids
    block_list = []

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
            if any(word in data for word in check1) \
            and not any(ad_id in data for ad_id in self.block_list):
                ret = Car()
                ret['url'] = response.url
                if "komfortzugang" in data:
                    ret['keyless'] = "Y"
                if "adaptive drive" in data:
                    ret['adaptive drive'] = "Y"
                yield ret
                
                
                
        #connectedDrive
        #adaptive drive
        #Keyless Drive / Keyless Vehicle
        #fahrerassistenz