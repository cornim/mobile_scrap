'''
Created on Aug 20, 2015

@author: corni
'''

from scrapy import Spider, Request
from tutorial.items import Car

class VolvoSpider(Spider):
    name = "all"
    allowed_domains = ["mobile.de"]
    start_urls = [
                  "http://suchen.mobile.de/fahrzeuge/auto/search.html?categories=EstateCar&transmissions=AUTOMATIC_GEAR&scopeId=C&damageUnrepaired=NO_DAMAGE_UNREPAIRED&fuels=DIESEL&minFirstRegistrationDate=2010-01-01&minPrice=15000&maxPrice=16000&maxMileage=125000&minPowerAsArray=110&minPowerAsArray=KW&isSearchRequest=true&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING",
                  "http://suchen.mobile.de/fahrzeuge/auto/search.html?categories=EstateCar&transmissions=AUTOMATIC_GEAR&scopeId=C&damageUnrepaired=NO_DAMAGE_UNREPAIRED&fuels=DIESEL&minFirstRegistrationDate=2010-01-01&minPrice=16000&maxPrice=17000&maxMileage=125000&minPowerAsArray=110&minPowerAsArray=KW&isSearchRequest=true&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING",
                  "http://suchen.mobile.de/fahrzeuge/auto/search.html?categories=EstateCar&transmissions=AUTOMATIC_GEAR&scopeId=C&damageUnrepaired=NO_DAMAGE_UNREPAIRED&fuels=DIESEL&minFirstRegistrationDate=2010-01-01&minPrice=17000&maxPrice=18000&maxMileage=125000&minPowerAsArray=110&minPowerAsArray=KW&isSearchRequest=true&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING",
                  "http://suchen.mobile.de/fahrzeuge/auto/search.html?categories=EstateCar&transmissions=AUTOMATIC_GEAR&scopeId=C&damageUnrepaired=NO_DAMAGE_UNREPAIRED&fuels=DIESEL&minFirstRegistrationDate=2010-01-01&minPrice=18000&maxPrice=19000&maxMileage=125000&minPowerAsArray=110&minPowerAsArray=KW&isSearchRequest=true&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING",
                  "http://suchen.mobile.de/fahrzeuge/auto/search.html?categories=EstateCar&transmissions=AUTOMATIC_GEAR&scopeId=C&damageUnrepaired=NO_DAMAGE_UNREPAIRED&fuels=DIESEL&minFirstRegistrationDate=2010-01-01&minPrice=19000&maxPrice=20000&maxMileage=125000&minPowerAsArray=110&minPowerAsArray=KW&isSearchRequest=true&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING"
    ]

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
            check1 = ("aktive geschw", "adaptive cruise control", "abstandsregelung", "abstandregelung"
                      "driving assistant plus", "fahrerassistenz-paket", "fahrerassistenz paket",
                      "fahrassistenz-paket", "fahrassistenz paket", "abstandsregeltempomat")
            check2 = ("keyless go", "keyless drive", "keyless vehicle", "komfortzugang")
            if any(word in data for word in check1) and any(word in data for word in check2):
                ret = Car()
                ret['url'] = response.url
                yield ret

         
                
        #connectedDrive
        #adaptive drive
        #Keyless Drive / Keyless Vehicle
        #fahrerassistenz