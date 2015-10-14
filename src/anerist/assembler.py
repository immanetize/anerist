from anerist.file_handlers import file_handlers
from anerist.meta import validator

hander = file_handlers()
validator = validator()

class assemble():
    def collect_json(self, target):
        collection = []
        for json in target:
            meta = file_handlers.load_json(metadata=json)
            for data in meta:
                if validator.validate(data):
                    collection.append(data)
        return collection
            

