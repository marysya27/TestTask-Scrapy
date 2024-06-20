import scrapy
from test_task.items import RentItem
import re

class KelmSpider(scrapy.Spider):
    name = 'kelm'
    start_urls = ['https://kelm-immobilien.de/immobilien/page/4/']
      
    def parse(self, response):
        links = response.xpath('//div[@class="property-details col-sm-12 vertical"]/h3/a/@href').getall()

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_each_link)


    def parse_each_link(self, response):
        item = RentItem()
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="immomakler-single immomakler"]/h1/text()').get()
        item['status'] = response.xpath('//div[@class="col-xs-12 col-sm-5 col-sm-pull-7"]/div[@class="property-details panel panel-default"]/ul[@class="list-group"]/li[@class="list-group-item data-zustand"]/div[@class="row"]/div[@class="dd col-sm-7"]/text()').get()

        pictures_resp = response.xpath('//div[@id="immomakler-galleria"]/a/img/@srcset').getall()
        array_pictures = [picture.split(',') for picture in pictures_resp]

        pattern = r'https://[^\s]+\.jpg'
        result_pictures = [re.search(pattern, i[-1]).group() for i in array_pictures]

        item['pictures'] = result_pictures
        
        item['rent_price'] = float(response.xpath('//li[@class="list-group-item data-kaufpreis"]/div[@class="row price"]/div[@class="dd col-sm-7"]/text()').get()[:-4])
        if not item['rent_price']:
            item['rent_price'] = float(response.xpath('//li[@class="list-group-item data-kaltmiete"]/div[@class="row price"]/div[@class="dd col-sm-7"]/text()').get()[:-4])

        description = response.xpath('//div[@class="property-description panel panel-default"]/div[@class="panel-body"]/p/text()').getall()
        item['description'] = '\n'.join(description).strip()
        item['phone_number'] = response.xpath('//div[@class="dd col-sm-7 p-tel value"]/a/text()').get()
        item['email'] = response.xpath('//div[@class="dd col-sm-7 u-email value"]/a/text()').get()
        item['country'] = 'Germany'  
        item['domain'] = 'kelm-immobilien.de' 

        yield item
