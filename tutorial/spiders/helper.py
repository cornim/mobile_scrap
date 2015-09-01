'''
Created on Aug 31, 2015

@author: corni
'''

import re
import logging

def search_words_yes_no(words, data, car_item, car_field):
    if any(word in data for word in words):
        car_item[car_field] = "Y"
    else:
        car_item[car_field] = "N"
        
def extract_main_data(response, car_item):
    main_data = "".join(response.xpath("//div[@class='mainTechnicalData']/p/text()").extract())
    try:
        ez_match = re.match(r".*([0-9]{2}).([0-9]{4}).*", main_data, flags=re.DOTALL)
        car_item['ez'] = int(ez_match.group(2)) + int(ez_match.group(1))/12.0
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
        