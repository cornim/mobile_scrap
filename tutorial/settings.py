# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
from scrapy.settings.default_settings import ITEM_PIPELINES

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'
USER_AGENT = 'test,1.0'

DOWNLOAD_HANDLERS = {'s3': None,}

LOG_LEVEL = 'INFO'
#LOG_FILE = 'scrapy.log'

ITEM_PIPELINES = {
    'tutorial.pipelines.CarPipeline' : 500
    }

