# -*- coding: utf-8 -*-
import scrapy
from meinv.items import MeinvItem
import time
import os
from scrapy import Request


class GirlsSpider(scrapy.Spider):
    name = 'girls'
    allowed_domains = ['55156.com']
    start_urls = [
        # 'http://www.55156.com/meinvtupian/',
        # 'http://www.55156.com/gaoqingtaotu/',
        # 'http://www.55156.com/weimeiyijing/',
        'http://www.55156.com/katongdongman/',
    ]

    # 图集数量
    album_count = 0

    def parse(self, response):
        """
        获取全部图集的url，得到图集的title  及 url
        :param response:
        :return:
        """
        items = MeinvItem()
        a_tag_list = response.xpath('//div[@class="listBox"]/ul/li/a')
        for a_tag in a_tag_list:
            album_url = a_tag.xpath('@href')[0].extract()
            album_title = a_tag.xpath('@title')[0].extract()
            items['album_url'] = album_url
            items['album_title'] = album_title
            tag = response.url.split('/')[3]
            items['tag'] = tag
            self.album_count += 1
            yield Request(album_url,callback=self.parse_album,meta={
                'album_url': items['album_url'],
                'album_title': items['album_title'],
                'tag': items['tag']

            })

        next_page_status = response.xpath('//div[@class="pages"]/ul/li[last()-1]/a/text()')[0].extract()
        if "下一页" in next_page_status:
            next_page = response.xpath('//div[@class="pages"]/ul/li[last()-1]/a/@href')[0].extract()
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url,callback=self.parse)
            time.sleep(1)
        items['album_count'] = self.album_count
        yield items['album_count']

        print('*******************%s共有  %s  套 ' % (tag,items['album_count']))

    def parse_album(self,response):
        """
        获取单个图片的url  及  title    通过meta传递 来的图集title 及 url 对应关系
        :param response:
        :return:
        """
        item = MeinvItem()
        img_url = response.xpath('//div[@class="articleBody"]/p/a/img/@src')[0].extract()
        img_title = response.xpath('//div[@class="articleBody"]/p/a/img/@alt')[0].extract()
        item['image_title'] = img_title
        item['image_url'] = img_url
        item['album_title'] = response.meta['album_title']
        item['album_url'] = response.meta['album_url']
        item['tag'] = response.meta['tag']
        yield item
        yield Request(img_url, callback=self.SaveImage, meta={
            'album_title': item['album_title'],
            'img_title': item['album_title'],
        })

        status = response.xpath('//div[@class="pages"]/ul').extract()
        next_page = response.xpath('//div[@class="pages"]/ul/li[last()]/a/@href').extract()
        if status:
            if next_page:
                if '#' not in next_page[0]:
                    next_url = response.urljoin(next_page[0])
                    yield Request(next_url,callback=self.parse_album,meta={
                        'album_title': item['album_title'],
                        'album_url': item['album_url'],
                        'tag': item['tag']
                    })
                else:
                    print('*************最后一页了 别翻了 ***********')
            else:
                print('******* 找不到下一页  %s图集只有一张图片*********' %response.meta['album_url'])

    def SaveImage(self,response):
        """
        保存图片到本地
        :param response:
        :return:
        """
        album_title = response.meta['album_title']
        img_title = response.meta['img_title']
        # 拼接保存图片的路径
        path = os.path.abspath('.') + '\\xiaojiejie\\' + album_title +'\\'
        if not os.path.exists(path):
            os.makedirs(path)

        file = path + img_title + '.jpg'
        with open(file,'wb') as f:
            f.write(response.body)
            print('%s **** 图片写入成功' % img_title)


