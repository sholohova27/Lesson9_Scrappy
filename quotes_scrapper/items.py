import scrapy


class AuthorItem(scrapy.Item):
    fullname = scrapy.Field()
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field()


class QuoteItem(scrapy.Item):
    quote = scrapy.Field()
    tags = scrapy.Field()
    author = scrapy.Field()

