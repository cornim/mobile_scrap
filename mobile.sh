#!/bin/bash

cd /home/corni/workspace/mobile_scrap

python /home/corni/workspace/mobile_scrap/scrapy/cmdline.py crawl bmw

sleep 20

python /home/corni/workspace/mobile_scrap/scrapy/cmdline.py crawl volvo

