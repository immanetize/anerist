from docutils.core import publish_programmatically as pp
from docutils.readers.standalone import Reader
from docutils.parsers.rst import Parser
from docutils.writers.pep_html import Writer
from docutils.frontend import Values
#from docutils import SettingsSpec

reader = Reader()
parser = Parser()
writer = Writer()
settings = Values()
f = open('/home/pete/docs/rst_article_sets/infra-docs/dns.rst', 'r')

doc = pp(
        source_class = "io.FileInput",
        source = f,
        source_path = None, # /path/to/file, pair with source=None
        destination_class = "io.StringOutput",
        destination = None,
        destination_path = None,
        reader = reader,
        reader_name = None, #alias if no reader supplied
        parser = parser,
        parser_name = None, #alias if no reader supplied
        writer = writer,
        writer_name = None, #alias if no reader supplied
        settings = settings,
        settings_spec = None, #used only if settings is not specified
        settings_overrides = None, # used only if settings is not specified
        config_section = None, #used only if settings is not specified
        enable_exit_status = False
    )


