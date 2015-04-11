import argparse
import ConfigParser
from anerist import extractors
import sys

class Cli(object):
    def __init__(self):
        self.args = self.parse_args()

    def update_metadata(
            publican_config="publican.cfg", 
            metadata_file="metadata.yml",
            lang="en-US",
            ):
        title, stub, abstract = extractors._read_publican_config(publican_config, lang)
        meta = extractors._load_yaml(metadata_file)
        meta['title'] = title
        meta['stub'] = stub
        meta['abstract'] = abstract
        extractors._write_yaml(meta, metadata)
    
    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = "A multipurpose toolkit for processing documentation metadata",
            epilog = "This utility is part of the anerist project"
            )
        subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')
        subparsers.required = True
        update_parser = subparsers.add_parser(
            'update_metadata',
            help = """
            Extracts information from the native format and inserts
            into a YAML metadata descriptor file.
            """,
            )
        update_parser.add_argument(
            '-p', 
            '--publican_config',
            help = "Publican config file to read from.  Defaults to 'publican.cfg'",
            default = 'publican.cfg',
            type = argparse.FileType('r')
            )
        update_parser.add_argument(
            '-m',
            '--metadata_file',
            help = "metadata file to update.  Defaults to 'metadata.yml'",
            type = argparse.FileType('w')
            )
        return parser.parse_args()

    def run(self):
        self.args.func()
        
def main():
    try:
        cli = Cli()
        cli.run()
    except KeyboardInterrupt:
        print("Interrupted, exiting...")
        sys.exit(1)

if __name__ == '__main__':
    main()


       
