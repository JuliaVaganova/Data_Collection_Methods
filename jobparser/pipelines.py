# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies120222

    def process_item(self, item, spider):
        if spider.name == 'sjru':
            salary = self.process_salary_sj(item.get('salary'))
        else:
            salary = self.process_salary_hh(item.get('salary'))

        item['salary_min'], item['salary_max'], item['cur'] = salary
        del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    @staticmethod
    def process_salary_hh(dirty_salary):
        salary_min = None
        salary_max = None
        cur = None
        dirty_salary = dirty_salary.replace(u'\xa0', u'').replace(u'\u202f', u'')
        salary_prep1 = re.sub('–', '', dirty_salary)
        salary_prep2 = re.split(r'\s+', salary_prep1)
        if salary_prep2[0] == 'от':
            salary_min = int(salary_prep2[1])
            salary_max = None
        elif salary_prep2[0] == 'до':
            salary_min = None
            salary_max = int(salary_prep2[1])
        else:
            salary_min = int(salary_prep2[0])
            salary_max = int(salary_prep2[1])
        cur = salary_prep2[2]
        return salary_min, salary_max, cur

    @staticmethod
    def process_salary_sj(dirty_salary):
        salary_min = None
        salary_max = None
        cur = 'руб'

        if dirty_salary[0] == 'до':
              salary_max = int(''.join(filter(str.isdigit, dirty_salary[2].replace(u'\xa0', u''))))
        elif dirty_salary[0] == 'от':
              salary_min = int(''.join(filter(str.isdigit, dirty_salary[2].replace(u'\xa0', u''))))
        elif len(dirty_salary) > 3 and dirty_salary[0].isdigit():
              salary_min = int(''.join(filter(str.isdigit, dirty_salary[0].replace(u'\xa0', u''))))
              salary_max = int(''.join(filter(str.isdigit, dirty_salary[4].replace(u'\xa0', u''))))
        else:
            cur = None
        return salary_min, salary_max, cur
