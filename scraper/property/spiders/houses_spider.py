import scrapy


class HouseSpider(scrapy.Spider):
    name = 'houses'

    start_urls = ['https://ikman.lk/en/ads/sri-lanka/houses?categoryType=ads&categoryName=Property']

    def parse(self, response):
        houses = response.css('div.ui-item')
        for house in houses:
            yield {
                'title': house.css('.h4::text').extract_first(),
                'price': house.css('p.item-info strong::text').extract_first(),
                'rooms': house.css('p.item-meta span::text').extract()
            }

        next_page  = response.css('div.lg-g div.lg-g a::attr(href)').extract_first()

        if next_page is not None:
            print("not nonw")
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)