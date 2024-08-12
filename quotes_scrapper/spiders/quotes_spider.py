import scrapy
from quotes_scrapper.items import QuoteItem, AuthorItem



class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css("div.quote"):
            quote_item = QuoteItem()
            quote_item['quote'] = quote.css("span.text::text").get()
            quote_item['tags'] = quote.css("div.tags a.tag::text").getall()
            quote_item['author'] = quote.css("span small.author::text").get()
            author_link = quote.css("span a::attr(href)").get()
            author_url = response.urljoin(author_link)

            # Запрашиваем информацию об авторе
            yield scrapy.Request(author_url, callback=self.parse_author, meta={'quote_item': quote_item})

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        author_item = AuthorItem()

        author_item['fullname'] = response.css("h3.author-title::text").get().strip()
        author_item['born_date'] = response.css("span.author-born-date::text").get().strip()
        author_item['born_location'] = response.css("span.author-born-location::text").get().strip()
        author_item['description'] = response.css("div.author-description::text").get().strip()

        yield author_item
        yield quote_item
