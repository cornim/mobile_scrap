'''
Created on Aug 20, 2015

@author: corni
'''

from tutorial.items import Car
from tutorial.spiders.all import CarSpider

class VolvoSpider(CarSpider):
    name = "volvo"
    allowed_domains = ["mobile.de"]
    start_urls = [
        "http://suchen.mobile.de/auto/search.html?isSearchRequest=true&sortOption.sortOrder=ASCENDING&scopeId=C&sortOption.sortBy=searchNetGrossPrice&damageUnrepaired=NO_DAMAGE_UNREPAIRED&minFirstRegistrationDate=2009-01-01&maxMileage=150000&maxPrice=25000&fuels=DIESEL&makeModelVariant1.makeId=25100&makeModelVariantExclusions[0].makeId=25100&makeModelVariantExclusions[0].modelId=32&makeModelVariantExclusions[1].makeId=25100&makeModelVariantExclusions[1].modelId=41&categories=EstateCar&transmissions=AUTOMATIC_GEAR&minPowerAsArray=110&maxPowerAsArray=KW&minPowerAsArray=KW&ambitCountry=DE"
    ]
    
    def __init__(self, *args, **kwargs):
        super(VolvoSpider, self).__init__(*args, **kwargs)
        
    fname = "volvo_blocked_ids"

    def parse_car(self, response):
        data = response.xpath("//div[@id='ad-description']").extract()
        if len(data)==1:
            data = data[0].lower()
            check1 = ("aktive geschw", "adaptive cruise control", "abstandsregelung",  "abstandregelung"
                      "driving assistant plus", "fahrerassistenz-paket", "fahrerassistenz paket",
                      "fahrassistenz-paket", "fahrassistenz paket", "abstandsregeltempomat")
            if any(word in data for word in check1):
                ret = Car()
                
                self.extract_main_data(response, ret)
                
                self.search_words_yes_no(["komfortzugang", "keyless"], data, ret, 'keyless')
                self.search_words_yes_no(["adaptive drive"], data, ret, 'adaptive_drive')
                self.search_words_yes_no(["driving assistant plus", "stauassistent"], data, ret, 'stau_assi')
                self.search_words_yes_no(["rtti", "traffic information"], data, ret, 'RTTI')
                ret['m_paket'] = "N"
                
                ret['dist'] = self.plz_dist(response, "60314")
                
                ret['price'] = response.xpath("//p[contains(@class, 'pricePrimaryCountryOfSale priceGross')]/text()").extract()[0]
                ret['url'] = response.url
                yield ret
