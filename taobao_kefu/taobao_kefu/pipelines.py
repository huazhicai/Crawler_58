# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis


class RedisStartUrlPipeline(object):
    """
    把详情页链接保存到 redis（kefu:start_urls）
    """
    def __init__(self, host, port, db):
        self.redis_cli = redis.StrictRedis(
            host=host, port=port, db=db
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('REDIS_HOST'),
            port=crawler.settings.get('REDIS_PORT'),
            db=crawler.settings.get('REDIS_DB'),
        )

    def process_item(self, item, spider):
        if type(item).__name__ == 'UrlItem':
            self.redis_cli.sadd(spider.redis_key, item['url'])
            spider.logger.info(
                'Successfully push start_urls to REDIS with url {}'.format(item['url'])
            )
            return item


class TaobaoKefuPipeline(object):
    def process_item(self, item, spider):
        return item
