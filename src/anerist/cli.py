import argparse
import ConfigParser
from anerist import extractors
import sys
import os

rest_machine = extractors.rest()
docbook_machine = extractors.docbook()
file_machine = extractors.file_handlers()

class Cli(object):
    def __init__(self):
        self.args = self.parse_args()

    #def extract(self, markup, output, target, lang):
    def extract(self):
        markup = self.args.markup
        output = self.args.output
        target = self.args.target
        lang = self.args.lang
        print(markup)
        if markup == 'rest':
            print(markup)
            metadata = rest_machine.read_broker(target, lang)
        elif markup == 'docbook':
            metadata = docbook_machine.read_broker(target, lang)
        elif markup == 'detect':
            print("Markup detection support is not yet available, please specify.")
            sys.exit()
        else:
            print("Something went wrong")
        file_machine.write_json(metadata, output)     
    
    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = "A multipurpose toolkit for processing documentation metadata",
            epilog = "This utility is part of the anerist project"
            )
        subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')
        subparsers.required = True
        update_parser = subparsers.add_parser(
            'extract',
            help = """
            Extracts information from the native format and inserts
            into a YAML metadata descriptor file.
            """,
            )
        update_parser.set_defaults(func=self.extract)
        update_parser.add_argument(
            '-m', 
            '--markup',
            help = "Markup format of files being extracted.",
            default = 'detect',
            choices = ['docbook', 'rest', 'detect']
            )
        update_parser.add_argument(
            '-o',
            '--output',
            help = "metadata file for output.  Defaults to 'metadata.json'",
            default = os.path.join(os.getcwd(), 'metadata.json'),
            )
        update_parser.add_argument(
            '-l',
            '--lang',
            help = 'language of input target',
            choices = ['en-US'],
            default = 'en-US'
            )
        update_parser.add_argument(
            'target',
            help = 'files or path to extract',
            nargs = '*',
            default = '%s' % os.getcwd(),
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


       
