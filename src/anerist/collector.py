import os
import copy
from anerist import file_handlers

file_machine = file_handlers.file_handlers()

class collector():
    aggregate_metadata = []

    def collect(self, target, scope):
        self.aggregate_metadata = self.get_aggregate(target)
        if scope == "all":
            return self.aggregate_metadata
            
    def get_aggregate(self, target):
        """
        Walks a list of provided paths (or files) for anerist-compatible 
        JSON metadata.  If paths are provided instead of absolute filenames,
        only files ending in ".json" will be matched.

        After discovering files, the collector opens each to return a python 
        object containing all discovered metadata.
        """

        meta_files = []
        aggregate_metadata = []
        for path in target:
            for root, dir, files in os.walk(path):
                for name in files:
                    if name.endswith(".json"):
                        meta_file = os.path.join(root, name)
                        meta_files.append(meta_file)
        for meta_file in meta_files:
            metadata = file_machine.load_json(metadata=meta_file)
            aggregate_metadata.extend(metadata)
        return aggregate_metadata

    def sitemap(self, aggregate_metadata):
    heirarchy_structure = { "children": {}, "contents": [] }
    for doc in aggregate_metadata:
        categories = doc['taxonomy'].split('/')
        depth = len(categories)
        try:
            heirarchy
        except NameError:
            heirarchy = copy.deepcopy(heirarchy_structure)
        working_heirarchy = heirarchy    
        while len(categories):
            category = categories[0]
            if not working_heirarchy['children'].get(category):
                    working_heirarchy['children'][category] = copy.deepcopy(heirarchy_structure)
            working_heirarchy = working_heirarchy['children'][category]
            print("removing %s" % category)
            categories.remove(category)
        working_heirarchy['contents'].append(doc['title'])
