import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class TranscriptsSpider(CrawlSpider):
    """
    A spider that crawls the 'subslikescript.com' website to extract movie transcripts.
    """

    # Name of the spider
    name = "transcripts"

    # Domains that are allowed to be crawled
    allowed_domains = ["subslikescript.com"]

    # Initial URLs to start crawling from
    start_urls = ["https://subslikescript.com/movies"]

    # Custom settings for the spider
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5  # Delay between requests to avoid overwhelming the server
    }

    # Rules for crawling and extracting links
    rules = (
        # Extract links to individual movie pages and parse them with the 'parse_item' method
        Rule(LinkExtractor(restrict_xpaths=('//ul[contains(@class, "scripts-list")]//li/a')), callback="parse_item", follow=True),
        # Extract links to the next page of the movie list and follow them
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class="pagination"]/li/a[@rel="next"]')), follow=True),
    )

    def parse_item(self, response):
        """
        Parses the response from a movie page to extract the title, plot, and URL.

        :param response: The HTTP response object from the crawled page
        :return: A dictionary containing the extracted data
        """
        article = response.xpath('//article[@class="main-article"]')
        yield {
            'title': article.xpath('./h1').get(),  # Extracts the movie title
            'plot': article.xpath('./p').get(),    # Extracts the movie plot
            'url': response.url                    # The URL of the current page
            # 'transcript': article.xpath('./div[@class="full-script"]//p[@class="cue-line"]/text()').getall(),
        }
        # Uncomment the line below to print the full transcript of the movie
        # print(article.xpath('./div[@class="full-script"]//p[@class="cue-line"]/text()').getall())