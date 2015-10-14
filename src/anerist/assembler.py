from anerist.file_handlers import file_handlers

hander = file_handlers()

class assemble():
    def collect_json(self, target):
        collection = []
        for json in target:
            meta = file_handlers.load_json(metadata=json)
            for data in meta:
                collection.append(data)
        return collection
            

