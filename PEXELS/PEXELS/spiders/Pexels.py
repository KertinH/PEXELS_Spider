# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import PexelsItem


class PexelsSpider(CrawlSpider):
    name = 'Pexels'
    allowed_domains = ['pexels.com']
    start_urls = ['https://www.pexels.com/']

    rules = (
        Rule(LinkExtractor(allow=r'^https://www.pexels.com/photo/.*/$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = PexelsItem()
        i['file_urls'] = response.xpath('.//img[contains(@src,"http")]/@src').extract()
        return i
