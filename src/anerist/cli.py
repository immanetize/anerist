import argparse
import ConfigParser
from anerist import extractors, file_handlers, collector
import sys
import os

rest_machine = extractors.rest()
docbook_machine = extractors.docbook()
file_machine = file_handlers.file_handlers()


def extra_args(extras=None, returntype="string"):
    """
    Utility function for processing the "--extra-args" argument to the 
    anerist extractor.  Intended for use with programatic invocation of anerist.

    The returntype declaration is required because this function does double duty,
    both preparing and validating command line arguments, and later processing those
    arguments into a format that's friendly for inclusion in document metadata.
    
    Markup processors must optionally accept an extra-args dict, and override 
    discovered metadata with their values.  For example, given a content file obviously 
    titled "Timmy Goes Fishing", an extra-args input like this:

    extra-args = { "title": "Timmy Goes on a Boat Ride" }

    must result in final metadata representing the latter title.

    """
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
    
    def collect(self):
        target = self.args.target
        output = self.args.output
        aggregate_metadata = collector.collect(target)
        file_machine.write_json(aggregate_metadata, output)
    #def extract(self, markup, output, target, lang):
    def extract(self):
        markup = self.args.markup
        output = self.args.output
        target = self.args.target
        lang = self.args.lang
        extra = extra_args(self.args.extra_args, returntype="dict")
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
    
    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = "A multipurpose toolkit for processing documentation metadata",
            epilog = "This utility is part of the anerist project"
            )
        subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')
        subparsers.required = True
        collect_parser = subparsers.add_parser(
            'collect',
            help = """
                Collects JSON format metadata and prepares it.
                """
            )
        collect_parser.set_defaults(func=self.collect)
        collect_parser.add_argument(
            'target',
            help = 'files or path to collect',
            nargs = '*',
            default = [os.getcwd()],
            )
        collect_parser.add_argument(
            '-o',
            '--output',
            help = "metadata file for output.  Defaults to 'aggregate_metadata.json'",
            default = os.path.join(os.getcwd(), 'aggregate_metadata.json'),
            )
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
            '-x',
            '--extra-args',
            help = "Extra arguments for metadata",
            default = None,
            type = extra_args
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
            default = [os.getcwd()],
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


       
