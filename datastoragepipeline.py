import json
from bson import json_util

class DataStoragePipeline(object):
    def open_spider(self, spider):
        self.file = open('resultsDetailed.json', 'w', encoding='utf-16')
        self.data = {"items": []}

    def close_spider(self, spider):
        self.data["count"] = len(self.data["items"])
        self.file.write(json.dumps(self.data, default=json_util.default, ensure_ascii=False, indent=4))
        self.file.close()

    def process_item(self, item, spider):
        self.data["items"].append(item)
        return item