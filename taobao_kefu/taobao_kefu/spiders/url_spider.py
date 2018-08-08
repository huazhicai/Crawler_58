# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import UrlItem


class UrlSpiderSpider(CrawlSpider):
    name = 'url_spider'
    redis_key = "url_spider:start_urls"

    def start_requests(self):
        citys = ['hz', 'jh', 'nb', 'wz', 'jx', 'tz', 'sx', 'huzhou', 'lishui', 'quzhou', 'zhoushan',
                 'yueqingcity', 'ruiancity', 'yiwu', 'yuyao', 'zhuji', 'xiangshanxian', 'wenling', 'tongxiang',
                 'cixi', 'changxing', 'jiashanx', 'haining', 'deqing', 'dongyang', 'anji', 'cangnanxian',
                 'linhai', 'yongkang', 'yuhuan', 'pinghushi', 'haiyan', 'wuyix', 'shengzhou',
                 'xinchang', 'jiangshanshi', 'pingyangxian']

        start_urls = ['http://{}.58.com/zptaobaokefu/'.format(city) for city in citys]
        for url in start_urls:
            yield scrapy.Request(url)

    rules = (
        # response返回javascripts 格式,所以提取不到
        # Rule(LinkExtractor(restrict_xpaths=('//*[@id="content-box"]/div[12]/div/div[2]/a[position()>1]',)
        #                    ), follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="filterArea"]/ul/li[position()>1]')),
             callback='parse_directory'),
    )

    custom_settings = {
        'ITEM_PIPELINES': {
            'taobao_kefu.pipelines.RedisStartUrlPipeline': 100,
        },
    }

    def parse_directory(self, response):
        # self.logger.info("Crawling: %s" % response.url)
        base_url = 'http://qy.58.com/'
        urls = response.xpath('//*[@id="list_con"]/li')
        for url in urls:
            item = UrlItem()
            uid = url.xpath('.//div[@class="item_con job_comp"]/input/@uid').extract_first().split('_')[0]
            mingqi = url.xpath('.//div[@class="comp_name"]/i/@class').extract_first()
            if mingqi and 'mingqi' in mingqi:
                item['url'] = base_url + 'mq/' + uid + '/'
                yield item
            else:
                item['url'] = base_url + uid + '/'
                yield item
        next_page = response.xpath('//div[@class="pagesout"]/a[@class="next"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_directory)
