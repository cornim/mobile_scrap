'''
Created on Aug 20, 2015

@author: corni
'''

from tutorial.spiders.all import CarSpider
from tutorial.items import Car

class BmwSpider(CarSpider):
    name = "bmw"
    allowed_domains = ["mobile.de"]
    start_urls = [
        "http://suchen.mobile.de/auto/search.html?isSearchRequest=true&sortOption.sortBy=searchNetGrossPrice&fuels=DIESEL&sortOption.sortOrder=ASCENDING&features=HEAD_UP_DISPLAY&damageUnrepaired=NO_DAMAGE_UNREPAIRED&ambitCountry=DE&scopeId=C&transmissions=AUTOMATIC_GEAR&categories=EstateCar&maxMileage=150000&minPowerAsArray=150&minPowerAsArray=KW&minFirstRegistrationDate=2011-01-01&maxPrice=31000&makeModelVariant1.makeId=3500&makeModelVariant1.modelId=16%2C17%2C74%2C18%2C19%2C20%2C21%2C22%2C65%2C23%2C66%2C24%2C25%2C26%2C67%2C70&makeModelVariant1.modelGroupId=22"
    ]
    
    def __init__(self, *args, **kwargs):
        super(BmwSpider, self).__init__(*args, **kwargs)

    fname = "bmw_blocked_ids"
    
            
    def parse_car(self, response):
        data = response.xpath("//div[@id='ad-description']").extract()
        if len(data)==1:
            data = data[0].lower()
            check1 = ("aktive geschw", "adaptive cruise control", "acc", "abstandsregelung", "driving assistant plus")
            if any(word in data for word in check1):
                ret = Car()
                
                self.extract_main_data(response, ret) #ez, km, price
                
                #feat comf
                self.search_words_yes_no(["komfortzugang", "keyless"], data, ret, 'keyless')
                self.search_words_yes_no(['aerodynamikpaket', 'aerodynamik-paket', 'aerodynamik paket',
                                     'sportpaket', 'sport-paket', 'sport paket',
                                     'm-paket', 'm paket'], data, ret, 'm_paket')
                
                self.search_words_yes_no(["komfortsitze", "komfort-sitze", "komfort sitze"], data, ret, "komf_sitz")
                self.search_words_yes_no(["aktivsitze", "aktiv-sitze", "aktiv sitze"], data, ret, "act_sitz")
                self.search_words_yes_no(["soft close", "soft-close"], data, ret, "sc_auto")
                self.search_words_yes_no(["garagentor"], data, ret, "gt_oeff")
                self.search_words_yes_no(["gerkupplung"], data, ret, "ah_kupp")
                
                #feat drive
                self.search_words_yes_no(["adaptive drive"], data, ret, 'adap_drive')
                self.search_words_yes_no(["driving assistant plus", "stauassistent"], data, ret, 'stau_assi')
                self.search_words_yes_no(["heckklappenbe", "automatische heckklappe"], data, ret, "auto_h_k")
                self.search_words_yes_no(["fernlichtassi"], data, ret, "fl_assi")
                self.search_words_yes_no(["kurvenlicht"], data, ret, "adapt_kl")
                self.search_words_yes_no(["aktivlenkung", "aktiv-lenkung", "aktiv lenkung"], data, ret, "act_lenk")
                self.search_words_yes_no(["integral"], data, ret, "act_ilenk")
                
                #feat drive info
                self.search_words_yes_no(["rtti", "traffic information"], data, ret, 'RTTI')
                self.search_words_yes_no(["profes"], data, ret, "navi_prof")
                self.search_words_yes_no(["speed"], data, ret, "speed_l_i")
                self.search_words_yes_no(["spurwechsel"], data, ret, "sw_warn")
                
                self.search_words_yes_no(["fahrkamera", "fahr kamera", "fahr-kamera"], data, ret, "r_cam")
                self.search_words_yes_no(["surround"], data, ret, "s_view")
                self.search_words_yes_no(["parkassistent", "park-assistent", "park assistent"], data, ret, "p_assi")                
                
                ret['dist'] = self.plz_dist(response, "60314")

                ret['price'] = response.xpath("//p[contains(@class, 'pricePrimaryCountryOfSale priceGross')]/text()").extract()[0]
                ret['url'] = response.url
                yield ret
                