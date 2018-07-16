# -*- coding: utf-8 -*-
import unicodedata
import scrapy


class HouseSpider(scrapy.Spider):
    name = 'house'

    start_urls = [
        'https://ikman.lk/en/ads/sri-lanka/houses?categoryType=ads&categoryName=Property',
        'https://ikman.lk/en/ads/sri-lanka/houses?categoryType=ads&categoryName=Property&page=2',
        'https://ikman.lk/en/ads/sri-lanka/houses?categoryType=ads&categoryName=Property&page=3',
        'https://ikman.lk/en/ads/sri-lanka/houses?categoryType=ads&categoryName=Property&page=4',
        'https://ikman.lk/en/ads/sri-lanka/houses?categoryType=ads&categoryName=Property&page=5',
        'https://ikman.lk/en/ads/sri-lanka/houses?categoryType=ads&categoryName=Property&page=6',
        'https://ikman.lk/en/ads/sri-lanka/houses?categoryType=ads&categoryName=Property&page=7',
        'https://ikman.lk/en/ads/sri-lanka/houses?categoryType=ads&categoryName=Property&page=8'
    ]
    # response.css('div.row.lg-g a.col-6.lg-3.pag-next::attr(href)').extract()
    def parse(self, response):
        houses = response.css('div.ui-item')
        for house in houses:

            for href in house.css('div.item-content a::attr(href)').extract():
                print ("href ***********************", href)
                # response.urljoin(href)
                d = response.follow(href, self.parse_house)
                print(d)
            yield {
                'title': house.css('.h4::text').extract_first(),
                'price': house.css('p.item-info strong::text').extract_first(),
                'rooms': house.css('p.item-meta span::text').extract(),
                'location': house.css('p.item-location span.item-area::text').extract_first()
                # 'description' : d
            }

        next_page  = response.css('body.on-serp-categoryV2 div.app-content div.ui-panel-content.ui-panel-bloa.col-6.lg-3.pag-next::attr(href)').extract_first()

        if next_page is not None:
            print("not null")
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



    def parse_house(self, response):
        print("inside")
        def extract_with_css(query):
            return response.css(query).extract()

        description = extract_with_css('body.on-item-detail div.app-content div.item-detail div.lg-g div.item-description p::text');

        return description


    def preprocess(self, text):
        if text == None: return None
        return unicodedata \
            .normalize('NFKD', text) \
            .encode('ascii', 'ignore') \
            .replace('\n', '').replace('\t', '').strip()
