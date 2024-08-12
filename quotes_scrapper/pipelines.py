import mongoengine as m
from .items import QuoteItem, AuthorItem
from .models import Author, Quote

class QuotesPipeline:

    def open_spider(self, spider):
        try:
            m.connect(
                db='nataly-db',
                username='nataly-db',
                password='Y2FAaVc9S4eiADtz',
                host='mongodb+srv://cluster0.d0plr.mongodb.net',
                ssl=True
            )
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            spider.crawler.engine.close_spider(spider, "MongoDB connection failed")

    def process_item(self, item, spider):
        if isinstance(item, QuoteItem):
            author_name = item['author']
            author = Author.objects(fullname=author_name).first()
            if not author:
                author = Author(fullname=author_name)
                author.save()

            quote = Quote(
                quote=item['quote'],
                tags=item['tags'],
                author=author
            )
            quote.save()
        elif isinstance(item, AuthorItem):
            author = Author.objects(fullname=item['fullname']).first()
            if author:
                author.update(
                    born_date=item['born_date'],
                    born_location=item['born_location'],
                    description=item['description']
                )
            else:
                author = Author(
                    fullname=item['fullname'],
                    born_date=item['born_date'],
                    born_location=item['born_location'],
                    description=item['description']
                )
                author.save()
        return item
