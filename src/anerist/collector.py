import os
from anerist import file_handlers

file_machine = file_handlers.file_handlers()

def collect(target):
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
