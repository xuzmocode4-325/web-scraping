import scrapy


class WorldometerSpider(scrapy.Spider):
    name = "worldometer"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a')

        for country in countries:
            country_name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()
    
            # # absolute url
            # absolute_url = response.urljoin(link)
            # yield scrapy.Request(url=absolute_url)

            # relative url
            yield response.follow(url=link, callback=self.parse_country, meta={'country':country_name})

    
    def parse_country(self, response, **kwargs):
        country = response.request.meta['country']
        rows = response.xpath('(//div[@class="table-responsive"])[1]//tbody//tr')
        
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/text()').get()
            migrants = row.xpath('.//td[5]/text()').get()
            median_age = row.xpath('.//td[6]/text()').get()
            urban_population = row.xpath('.//td[10]/text()').get()
            global_population = row.xpath('.//td[12]/text()').get()
            global_rank = row.xpath('.//td[13]/text()').get()

            yield {
                'country': country,
                'year': year,
                'population': population,
                'migrants': migrants,
                'madian_age': median_age,
                'urban_population': urban_population,
                'global_population': global_population,
                'global_rank': global_rank
            }