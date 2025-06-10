# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import psycopg2
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class GettingStartedPipeline:
    def open_spider(self, spider):
        logging.warning('[PIPELINE] spider open ')
        pass

    def close_spider(self, spider):
        logging.warning('[PIPELINE] spider closed')
        pass

    def process_item(self, item, spider):
        return item


# pipelines.py


class PostgresPipeline:
    def open_spider(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres"
        )
        self.curr = self.conn.cursor()
        try:
            self.curr.execute("""
            CREATE TABLE scraped_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(100),
            tags TEXT
            );
            """)
            self.conn.commit()
        except psycopg2.OperationalError:
            pass

    def process_item(self, item, spider):
        try:
            self.curr.execute("""
                INSERT INTO scraped_data (title, author, tags)
                VALUES (%s, %s, %s)
            """, (
                item['text'],
                item['author'],
                ', '.join(item['tags'])
            ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise DropItem(f"Failed to insert item: {e}")
        return item

    def close_spider(self, spider):
        self.curr.close()
        self.conn.close()
