import scrapy
from scrapy.crawler import CrawlerProcess

class WinnerCompaniesSpider(scrapy.Spider):
    name = "winner_companies"
    start_urls = ["https://www.cmu.edu/swartz-center-for-entrepreneurship/events/mcginnis-venture-competition/past-winners.html"]

    def parse(self, response):
        # Loop through each competition element
        for competition in response.css('.grid.column2.boxes.js-list'):
            items = {}

            # Extract year, graduate track, and first place
            year = competition.css('h1::text').extract_first()
            #one more loop
            for compt in competition.css('div'):
                comptition = compt.css('h2 > strong::text').extract_first()

                first_place = compt.css('p:nth-child(1) > a > strong::text').extract_first()
                second_place = compt.css('p:nth-child(2) > a > strong::text').extract_first()
                second_place = compt.css('p:nth-child(3) > a > strong::text').extract_first()

                # Assign values to the items dictionary
                items['year'] = year
                items['graduate track'] = comptition
                items['first_place'] = first_place

                yield items



if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(WinnerCompaniesSpider)
    process.start()