import argparse
import ConfigParser
from anerist import extractors
from anerist import file_handlers
from anerist import assembler
import sys
import os

rest_machine = extractors.rest()
docbook_machine = extractors.docbook()
file_machine = file_handlers.file_handlers()

def extra_args(extras=None, returntype="string"):
    if not extras:
        return None
    d = {}
    s = ""
    for pair in extras.split(','):
        if not '=' in pair or pair.count('=') != 1:
            raise argparse.ArgumentTypeError(
                    "Unable to parse extra arguments. \
                            These should be comma separated key value pairs:\
                            '--extra-args \"branch=$branch,approver=noone\"'"
                            )
        key, value = pair.split('=')
        value = value.translate(None, '"\'')
        d[key] = value
        # we broke this down so maybe more validation could happen
    if returntype == "string":
        for key in d.keys():
            s = s + "%s=%s," % (key, d[key])
        s = s.strip(',')
        return s
    elif returntype == "dict":
        return d


class Cli(object):
    def __init__(self):
        self.args = self.parse_args()

    #def extract(self, markup, output, target, lang):
    def extract(self):
        markup = self.args.markup
        output = self.args.output
        target = self.args.target
        lang = self.args.lang
        extra = extra_args(self.args.extra_args, returntype="dict")
        #extra = {'three': 'tres', 'two': 'dos', 'one': 'uno'}
        #extra = {"extra": "true"}
        #extra=None
        if markup == 'rest':
            metadata = rest_machine.read_broker(target, lang, extra)
        elif markup == 'docbook':
            metadata = docbook_machine.read_broker(target, lang, extra)
        elif markup == 'detect':
            print("Markup detection support is not yet available, please specify.")
            sys.exit()
        else:
            print("Something went wrong")
        file_machine.write_json(metadata, output)     
    def assemble(self):
        target = self.args.target
        meta_list = []
        for root, dirs, files in os.walk(os.getcwd()):
            for name in files:
                if name.endswith("json"):
                    meta_list.append(os.path.join(root, name))
        toc = assember.do_work(target)

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = "A multipurpose toolkit for processing documentation metadata",
            epilog = "This utility is part of the anerist project"
            )
        subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')
        subparsers.required = True
        assemble_parser = subparsers.add_parser(
                'assemble'
                help = """
                Assembles json metadata from a given path.
                """,
                )
        assemble_parser.set_defaults(func=self.assemble)
        assemble_parser.add_argument(
            'target',
            help = "path to assemble."
            nargs = '*',
            default = os.getcwd(),
            )
        extract_parser = subparsers.add_parser(
            'extract',
            help = """
            Extracts information from the native format and inserts
            into a YAML metadata descriptor file.
            """,
            )
        extract_parser.set_defaults(func=self.extract)
        extract_parser.add_argument(
            '-m', 
            '--markup',
            help = "Markup format of files being extracted.",
            default = 'detect',
            choices = ['docbook', 'rest', 'detect']
            )
        extract_parser.add_argument(
            '-x',
            '--extra-args',
            help = "Extra arguments for metadata",
            default = None,
            type = extra_args
            )
        extract_parser.add_argument(
            '-o',
            '--output',
            help = "metadata file for output.  Defaults to 'metadata.json'",
            default = os.path.join(os.getcwd(), 'metadata.json'),
            )
        extract_parser.add_argument(
            '-l',
            '--lang',
            help = 'language of input target',
            choices = ['en-US'],
            default = 'en-US'
            )
        extract_parser.add_argument(
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


       
