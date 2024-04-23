import scrapy
from scrapy.crawler import CrawlerProcess
import pyairtable
from datetime import datetime


class WinnerCompaniesSpider(scrapy.Spider):
    name = "winner_companies"
    start_urls = [
        "https://www.cmu.edu/swartz-center-for-entrepreneurship/events/mcginnis-venture-competition/past-winners.html"]

    def parse(self, response):

        for competition in response.css('.grid.column2.boxes.js-list'):
            items = {}

            # Extract year, graduate track, and first place
            items['year'] = competition.css('h1::text').extract_first().split()[0]
            # one more loop
            for compt in competition.css('div')[1:]:
                items['competition'] = compt.css('h2 ::text').extract_first()

                try:
                    items['winner business'] = compt.css('p')[0].css(' ::text').extract()[2:-1][0]
                except:
                    items['winner business'] = ''
                try:
                    items['2nd place business'] = compt.css('p')[1].css(' ::text').extract()[2:-1][0]
                except:
                    items['2nd place business'] = ''
                try:
                    items['3rd place business'] = compt.css('p')[2].css(' ::text').extract()[2:-1][0]
                except:
                    items['3rd place business'] = ''

                items['lastupdate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                table.create(items)


if __name__ == '__main__':

    process = CrawlerProcess()
    process.crawl(WinnerCompaniesSpider)
    process.start()
