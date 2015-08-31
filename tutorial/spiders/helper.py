'''
Created on Aug 31, 2015

@author: corni
'''

def search_words_yes_no(self, words, data, car_item, car_field):
    if any(word in data for word in words):
        car_item[car_field] = "Y"
    else:
        car_item[car_field] = "N"