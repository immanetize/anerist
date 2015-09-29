# factory for publican books
from buildbot.process.factory import *

# Command Classes
class PublicanBuild(ShellCommand):
    name = "publican_build"
    haltOnFailure = 1
    flunkOnFailure = 1
    description = ["building"]
    descriptionDone = ["build complete"]
    def __init__(self, langs=["en-US"], formats=["html-single"], **kwargs):
        valid_publican_formats = [
                "drupal-book",
                "eclipse",
                "epub",
                "html",
                "html-desktop",
                "html-single",
                "man",
                "pdf",
                "txt",
                "xml"
                ]
        if not all(output_format in valid_publican_formats for output_format in formats):
            config.error("Unknown or invalid publican output format specified")
        command= [
            "/usr/bin/publican",
            "build",
            "--langs",
            ','.join(langs),\
            "--formats",
            ",".join(formats)
            ]
        ShellCommand.__init__(self, **kwargs)
        self.setCommand(command)
    def start(self):
        ShellCommand.start(self)
