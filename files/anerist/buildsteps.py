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



class ZanataPublicanPull(ShellCommand):
    name = "zanata pull"
    haltOnFailure = 1
    flunkOnFailure = 1
    description = ["pulling translations from Zanata"]
    descriptionDone = ["translations refreshed"]
    def __init__(self, zanata_username=None, zanata_api_key=None):
        if zanata_username is None or zanata_api_key is None:
            config.error("zanata_username and zanata_api_key are required")
        shellCommand.__init__(self, **kwargs)
        command = [
            "/usr/bin/zanata",
            "--username %s" % zanata_username,
            "--apikey %s" % zanata_api_key,
            "--transdir ./%s/" % lang,
            "--lang %s" % lang
            ]
        self.setCommand(command)
            
class PublicanClean(ShellCommand):    
    name = "publican clean"
    haltOnFailure = 1
    flunkOnFailure = 1
    description = ["clean up publican tempdirs"]
    descriptionDone = ["publican cleanup finished"]
    command = [
            "/usr/bin/publican",
            "clean"
            ]

class GitClean(ShellCommand):
     name = "git clean"
     haltOnFailure = 1
     flunkOnFailure = 1
     description = ["git clean"]
     descriptionDone = ["git cleanup complete"]
     command = [
             "/usr/bin/git",
             "clean",
             "-xdf"
             ]

class IntegratorCommit(ShellCommand):
    name = "integrator commit"
    haltOnFailure = 1
    flunkOnFailure = 1
    description = ["Integrator translation commit"]
    descriptionDone = ["Integrator commit processed"]
    command = [
            "/usr/bin/git",
            "commit",
            "-m",
            "\"Anerist Integrator translation commit\""
            ]

