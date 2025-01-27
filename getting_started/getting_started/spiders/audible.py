import scrapy


class AudibleSpider(scrapy.Spider):
    name = 'audible'
    allowed_domains = ['www.audible.com']
    start_urls = ['https://www.audible.com/search']

    def parse(self, response):
        product_container = response.xpath('//div[contains(@data-widget,"productList")]/div/span[2]/ul/li')

        for product in product_container:
            title = product.xpath('.//h3[contains(@class, "bc-heading")]/a/text()').get()
            subtitle = product.xpath('.//li[contains(@class, "subtitle")]/span/text()').get()
            author = product.xpath('.//li[contains(@class, "authorLabel")]/span/a/text()').getall()
            length = product.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get()
            release_date = str(product.xpath('.//li[contains(@class, "releaseDateLabel")]/span/text()').get()).strip().replace("\n", "")
            language = str(product.xpath('.//li[contains(@class, "languageLabel")]/span/text()').get()).strip().replace("\n", "")

            yield {
                'author': author,
                'title': title,
                'subtitle': subtitle,
                'length': length,
                'release_date': release_date,
                'language': language
            }

        pagination = response.xpath('//ul[contains(@class,"pagingElements")]')
        next_page_url = pagination.xpath('//span[contains(@class, "nextButton")]/a/@href').get()

        if next_page_url: 
            yield response.follow(url=next_page_url, callback=self.parse)


