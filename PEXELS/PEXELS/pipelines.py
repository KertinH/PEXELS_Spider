# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
from io import BytesIO
import sys
from scrapy.utils.misc import md5sum

class TheFilesPipeline(FilesPipeline):
    def file_downloaded(self, response, request, info):
        path = self.file_path(request, response=response, info=info)
        buf = BytesIO(response.body)
        checksum = md5sum(buf)
        file_size = sys.getsizeof(response.body)
        print(file_size,'************'*30)
        buf.seek(0)
        # self.store.persist_file(path, buf, info)
        #这里限制4M以下的图片不下载，可以在此基础上更改
        if file_size > 4194304:
            self.store.persist_file(path, buf, info)
            return checksum
        else:
            pass

    def file_path(self, request, response=None, info=None):
        file_name = request.url.split('/')[-1]
        if '.' not in file_name:
            file_name = file_name + '.png'
        return 'pexels/%s'%file_name

class PexelsPipeline(object):
    def process_item(self, item, spider):
        list = item['file_urls']
        item['file_urls'] = []
        for i in list:
            if '?' in i:
                item['file_urls'].append(i.split('?')[0])
            else:
                item['file_urls'].append(i)
        return item
