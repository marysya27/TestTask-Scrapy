# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import json

class TestTaskPipeline:
    def process_item(self, item, spider):
        country = item.get('country', 'unknown')
        domain = item.get('domain', 'unknown')
        rental_object = item.get('title', 'unknown')
        
        results_directory = 'results'
        if not os.path.exists(results_directory):
            os.makedirs(results_directory)

        path_to_directory = os.path.join(results_directory, country, domain)
        if not os.path.exists(path_to_directory):
            os.makedirs(path_to_directory)

        file_path = os.path.join(path_to_directory, f"{rental_object}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dict(item), f, ensure_ascii=False, indent=4)

        return item
