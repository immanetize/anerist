import os
from anerist import file_handlers

file_machine = file_handlers.file_handlers()

class collector():
    def read_broker(self, target):
        meta_files = []
        for path in target:
            for root, dir, files in os.walk(target):
                for name in file:
                    if name.endswith(".json"):
                        meta_file = os.path.join(root, name)
                        meta_files.append(meta_file)

