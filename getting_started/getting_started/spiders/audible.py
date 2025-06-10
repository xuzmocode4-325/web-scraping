import scrapy

# Defines a class named AudibleSpider that inherits from scrapy.Spider. 
# This class will contain all the scraping logic.
class AudibleSpider(scrapy.Spider): 
    """
    A Scrapy Spider for scraping audiobook information from Audible's search page.
    """

    # Sets the name of the spider. 
    # This name is used to run the spider from the command line.
    name = 'audible' 

    # Specifies the domains that the spider is allowed to crawl.
    # This prevents the spider from accidentally wandering off to other websites.
    allowed_domains = ['www.audible.com'] 

    # A list of URLs where the spider will begin crawling.   
    start_urls = ['https://www.audible.com/search']

    #The parse method is the heart of the spider. 
    # It's called for each URL in start_urls, and it's responsible for extracting the data.
    def parse(self, response):
        """
        Parses the response from the Audible search page to extract audiobook details.

        Args:
            response (scrapy.http.Response): The response object containing the HTML content of the page.

        Yields:
            dict: A dictionary containing the extracted audiobook details such as author, title, subtitle, length, release date, and language.
        """
        ## response.xpath(): Applies the XPath expression to the response (the HTML content of the page).
        product_container = response.xpath('//div[contains(@data-widget,"productList")]/div/span[2]/ul/li')

        for product in product_container:
            title = product.xpath('.//h3[contains(@class, "bc-heading")]/a/text()').get()
            subtitle = product.xpath('.//li[contains(@class, "subtitle")]/span/text()').get()
            author = product.xpath('.//li[contains(@class, "authorLabel")]/span/a/text()').getall()
            length = product.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get()
            release_date = str(product.xpath('.//li[contains(@class, "releaseDateLabel")]/span/text()').get()).strip().replace("\n", "")
            language = str(product.xpath('.//li[contains(@class, "languageLabel")]/span/text()').get()).strip().replace("\n", "")

            # The yield keyword returns a Python dictionary containing the extracted data for each product. 
            # Scrapy automatically handles this yielded data, typically saving it to a file.
            yield {
                'author': author,
                'title': title,
                'subtitle': subtitle,
                'length': length,
                'release_date': release_date,
                'language': language
            }

        # These lines handle pagination, allowing the spider to crawl multiple pages.
        pagination = response.xpath('//ul[contains(@class,"pagingElements")]')
        next_page_url = pagination.xpath('//span[contains(@class, "nextButton")]/a/@href').get()

        if next_page_url: 
            yield response.follow(url=next_page_url, callback=self.parse)


