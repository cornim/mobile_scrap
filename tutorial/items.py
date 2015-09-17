# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Car(Item):
    # define the fields for your item here like:
    # name = Field()
    #main
    price = Field()
    price_calc = Field()
    price_diff = Field()
    ez = Field()
    ps = Field()
    km = Field()
    dist = Field()
    color_o = Field()
    color_i = Field()
    
    url = Field()
    
    #feat comf
    keyless = Field()
    m_paket = Field()
    komf_sitz = Field()
    act_sitz = Field()
    sc_auto = Field() #Soft close
    gt_oeff = Field() #garagentor
    ah_kupp = Field() #anhaenger kupplung
    
    #feat drive
    adap_drive = Field()
    ddc = Field()
    stau_assi = Field()
    auto_h_k = Field()  #automatische heckklappe
    fl_assi = Field()
    adapt_kl = Field()  #kurven licht
    act_lenk = Field()
    act_ilenk = Field()
    
    #feat drive info
    HUD = Field()
    RTTI = Field()
    navi_prof = Field()
    speed_l_i = Field()
    sw_warn = Field()
    
    r_cam = Field()
    s_view = Field()
    p_assi = Field()
    
    
    
    
    
    
    
    
    
    
    
    