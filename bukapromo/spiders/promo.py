# -*- coding: utf-8 -*-
import scrapy


class PromoSpider(scrapy.Spider):
    name = 'promo'
    allowed_domains = ['www.bukalapak.com']

    def start_requests(self):
        yield scrapy.Request(url='https://www.bukalapak.com/promo/di-bawah-1-8-juta.html', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        })

    def parse(self, response):
        products = response.xpath("//ul[@class='products row-grid']/li/div/article")
        for product in products:
            yield {
                'title': product.xpath(".//div[@class='product-description']/h3/a/text()").get(),
                'url': response.urljoin(product.xpath(".//div[@class='product-description']/h3/a/@href").get()),
                'price': product.xpath(".//div[@class='product-price']/span[1]/span[2]/text()").get(),
                'rating': product.xpath(".//div[@class='product__rating']/span/span/text()").get(),
                # 'User-Agent': response.request.headers['User-Agent']
            }

        next_page = response.xpath(".//div[@class='pagination']/a[position() = last()]/@href").get()

        if next_page:
            next_page_link = response.urljoin(next_page)
            print(next_page_link)
            yield scrapy.Request(url=next_page_link, callback=self.parse)