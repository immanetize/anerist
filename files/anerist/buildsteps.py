# factory for publican books
from buildbot.process.factory import *

# Command Classes
class PublicanBuild(ShellCommand):
    name = "publican build",
    haltOnFailure = 1
    flunkOnFailure = 1
    description = ["building"]
    descriptionDone = ["build complete"]
    command= [
            "/usr/bin/publican",
            "build",
            "--langs %s" % ','.join(langs),\
            "--formats %s" % ",".join(formats)
            ]

class ZanataPublicanPull(ShellCommand):
    name = "zanata pull"
    haltOnFailure = 1
    flunkOnFailure = 1
    description = ["pulling translations from Zanata"]
    descriptionDone = ["translations refreshed"]
    command = [
            "/usr/bin/zanata",
            "--username %s" % zanata_username,
            "--apikey %s" % zanata_api_key,
            "--transdir ./%s/" % lang,
            "--lang %s" % lang
            ]
            
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

