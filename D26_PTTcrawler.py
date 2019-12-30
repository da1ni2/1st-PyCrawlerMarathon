# -*- coding: utf-8 -*-
import scrapy


class PttcrawlerSpider(scrapy.Spider):
    name = 'PTTcrawler'
    allowed_domains = ['https://www.ptt.cc/bbs/Lifeismoney/M.1577708135.A.B7B.html']
    start_urls = ['http://https://www.ptt.cc/bbs/Lifeismoney/M.1577708135.A.B7B.html/']

    def start_request(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url ,callback = self.parse , cookies={'over18' : {'1'}} )
    
    def parse(self, response):
        pass
