import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider):
    name = "transcripts"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies"]

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//ul[contains(@class, "scripts-list")]//li/a')), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class="pagination"]/li/a[@rel="next"]')), follow=True),
    )

    def parse_item(self, response):
        article = response.xpath('//article[@class="main-article"]')
        yield {
            'title' : article.xpath('./h1').get(), 
            'plot': article.xpath('./p').get(),
            'url': response.url
            #'transcript': article.xpath('./div[@class="full-script"]//p[@class="cue-line"]/text()').getall(),
        }
        # print(article.xpath('./div[@class="full-script"]//p[@class="cue-line"]/text()').getall())