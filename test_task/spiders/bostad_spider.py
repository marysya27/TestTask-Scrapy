import scrapy
from test_task.items import RentItem


class BostadSpider(scrapy.Spider):
    name = 'bostad'
    start_urls = ['https://bostad.herbo.se/HSS/Object/object_list.aspx?cmguid=4e6e781e-5257-403e-b09d-7efc8edb0ac8&objectgroup=1']
      
    def parse(self, response):
        links = response.xpath('//tr[starts-with(@class, "listitem-")]/td[@class="gridcell"]/a/@href').getall()

        for link in links:
            if link.startswith("ObjectDetails"):
                yield scrapy.Request(url='https://bostad.herbo.se/HSS/Object/'+link, callback=self.parse_each_link)


    def parse_each_link(self, response):
        item = RentItem()

        item['url'] = response.url
        item['title'] = response.xpath('//h1[@id="ctl00_ctl01_lblTitle"]/text()').get()
        item['status'] = None

        pictures_resp = response.xpath('//div[@id="ctl00_ctl01_DefaultSiteContentPlaceHolder1_Col1_divImageThumbs"]/img/@src').getall()
        item['pictures'] = ['https://bostad.herbo.se/'+pict for pict in pictures_resp]
        
        item['rent_price'] = float(response.xpath('//ul[@id="ctl00_ctl01_DefaultSiteContentPlaceHolder1_Col1_trCost"]/li[@class="right"]/text()').get()[:-3].replace(" ", ""))
        item['description'] = response.xpath('//div[@id="ctl00_ctl01_DefaultSiteContentPlaceHolder1_Col1_divOverview"]//p/text()').getall()
        item['phone_number'] = None
        item['email'] = None
        item['country'] = 'Sweden'  
        item['domain'] = 'bostad.herbo.se' 

        yield item
