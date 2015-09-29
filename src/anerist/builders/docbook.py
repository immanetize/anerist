from buildbot.steps.source.git import Git
#this needs to get moved to anerist cli!
from anerist.buildsteps import PublicanBuild
from buildbot.steps.shell import ShellCommand

# BIG TODO:
#
# I just realized this expects lists to be ordered just how I expect.  Don't do that.
    
class docbook_factory_generator():
    def __init__(self):
        pass
    
    def publican_build(self, langs, formats):
        new_step = []
        new_step.append(
            PublicanBuild(
                langs=langs,
                formats=formats
                )
            )
        return new_step

    def zanata_pull(self, resource_name, zanata_project, zanata_username, zanata_api_key, zanata_server, lang):
        new_step = []
        # TODO: this --transdir relative path seems unpredictable!
        zanata_command = [ 
            "/usr/bin/zanata",
            "--transdir ./%s./" % lang,
            "--lang %s" % lang
            ]
        if zanata_username:
            zanata_command.append("--username %s" % zanata_username)
        if zanata_api_key:
            zanata_command.append("--apikey '%s'" % zanata_api_key)

        # TODO:
        # this all assumes that the remote project and version has been set up on the server
        # that assumption could go away, and be done programatically.
        # It also assumes that a zanata.xml is available for the project, probably.
        # Investigate other zanata client command line switches.

        new_step.append(
            ShellCommand(
                name = "%s zanata pull",
                command = zanata_command,
                haltOnFailure = True
                )
            )

        return new_step

    def gen_pots(self, lang, resource_name):
        # TODO: make this use itstool
        new_step = []
        new_step.append(
            ShellCommand(
                name = "Refresh POTs for %s" % resource_name,
                command = ["/usr/bin/publican", "update_pot"],
                haltOnFailure=False
                 )
            )

        return new_step       
 
