import json
import yaml

class file_handlers():
    def write_json(self, meta, output="metadata.json"):
        f = open(output, 'w')
        printable_json = json.dumps(meta, encoding="utf-8", indent=3)
        f.write(printable_json)
        f.close()

    def load_json(self, metadata="metadata.json"):
        f = open(metadata, 'r')
        meta = json.loads(f.read())
        f.close()
        return meta

    def load_yaml(self, metadata="metadata.yml"):
        y = open(metadata)
        meta = yaml.load(y)
        y.close()
        return meta

    def write_yaml(self, meta, metadata="metadata.yml"):
        y = open('metadata.yml', 'w')
        yaml.dump(meta, y, default_flow_style=False)
        y.close()

