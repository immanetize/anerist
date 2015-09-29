from buildbot.steps.source.git import Git
#this needs to get moved to anerist cli!
from anerist.buildsteps import PublicanBuild
from buildbot.steps.shell import ShellCommand

# BIG TODO:
#
# I just realized this expects lists to be ordered just how I expect.  Don't do that.

    
class vcs_factory_generator():
    def __init__(self):
        pass
    
    def vcs_clean(self, resource_name, vcs_type, repourl):
        new_step = []
        if vcstype == "git":
            newstep.append(
                ShellCommand(                    
                    name = "%s git cleanup" % resource_name,
                    command = ["/usr/bin/git", "clean", "-xdf"]
                    )
                )
        return new_step
    
    def vcs_fetch(self, resource_name, vcs_type, repourl):
        new_step = []
        if vcstype == "git":
            newstep.append(
                Git(
                    name = "%s git fetch" % resource_name,
                    repourl = repourl,
                    mode = 'incremental'
                    )
                )
        return new_step
      
    def vcs_branch(self, vcs_type, branch_name):
        new_step = []
        if vcstype == "git":
            newstep.append(
                ShellCommand(
                    name = "git branch %s " % branch_name,
                    command = ["/usr/bin/git", "branch", branch_name],
                    mode = 'incremental'
                    )
                )
        return new_step
    
    def vcs_checkout(self, vcs_type, branch_name):
        new_step = []
        if vcstype == "git":
            newstep.append(
                ShellCommand(
                    name = "git checkout %s " % branch_name,
                    command = ["/usr/bin/git", "checkout", branch_name]
                    )
                )
        return new_step

    def vcs_merge(self, vcs_type, branch_name):
        new_step = []
        if vcstype == "git":
            newstep.append(
                ShellCommand(
                    name = "git merge %s " % branch_name,
                    command = ["/usr/bin/git", "merge", branch_name]
                    )
                )
        return new_step

    def vcs_commit(self, resource_name, vcs_type, repourl, commit_msg):
        new_step = []
        if vcstype == "git":
            newstep.append(
                ShellCommand(
                    name = "%s git commit" % resource_name,
                    command = ["/usr/bin/git", "commit", "-m", commit_msg]
                    )
                )

        return new_step
    
