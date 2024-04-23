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
    api = pyairtable.Api('patAutBB8czI3ifML.c1e5aa28bb6f09cbb0d81815494d371003902e6f43500abebe713f307a505f25')
    base = api.base('appISH2KhnZt5ElD8')
    table = [v for v in base.tables() if v.name == 'Main Table'][0]
    process = CrawlerProcess()
    process.crawl(WinnerCompaniesSpider)
    process.start()
