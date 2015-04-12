# -*- python -*-
# ex: set syntax=python:

from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.schedulers.forcesched import ForceScheduler
from buildbot.changes.filter import ChangeFilter
from buildbot.scheduler import Nightly

c = BuildmasterConfig = {}

####### BUILDSLAVES
from buildbot.buildslave import BuildSlave
c['slaves'] = [
        {% for host in groups['buildbot-slaves'] %}    
	    BuildSlave("{{ host }}", "{{ ansible_local.buildbot.pass.buildslave_pass }}"),
        {% endfor %}
	]
c['protocols'] = {'pb': {'port': 9989}}

from anerist.helpers import PublicanHelpers
from anerist.helpers import FedoraHelpers

jeff = PublicanHelpers()
mac = FedoraHelpers()
published_branches = mac.release_tracker()
published_branches.append('master')
guide_list = mac.published_publican_guides()
filtered_branches = ChangeFilter(
        branch_fn = published_branches
        )
translated_langs = jeff.valid_langs()

def _guide_git_url(guide):
    anon_url = "https://git.fedorahosted.org/git/docs/%s.git" % guide
#    ssh_url = "ssh://git.fedorahosted.org/git/docs/%s.git" % guide
    ssh_url = "ssh://buildbot@lemuria.home.randomuser.org:/srv/projects/docs/guides/%s" % guide
    return anon_url, ssh_url
  
####### CHANGESOURCES

from buildbot.changes.gitpoller import GitPoller
import random

c['change_source'] = []
for guide in guide_list:
    anon_url, ssh_url = _guide_git_url(guide)
    c['change_source'].append(GitPoller(
        anon_url, 
        workdir=guide, 
        branches=published_branches,
        pollinterval=random.randint(300,600)
        ))

####### BUILDERS

from buildbot.process.factory import BuildFactory
from buildbot.steps.source.git import Git
from buildbot.steps.shell import ShellCommand
from buildbot.process.factory import Publican
from buildbot.steps.transfer import DirectoryUpload
from buildbot.process.properties import Interpolate
from datetime import datetime
from anerist.buildsteps import *

def _publican_publisher_factory_step_generator(guide, langs=["en-US"], formats=["html-single"]):
    anon_url, ssh_url = _guide_git_url(guide)
    publican_factory_steps = [
            Git(
                name = "%s fetch" % guide,
                repourl=anon_url,
                mode='incremental'
                ),
            PublicanBuild(
                langs = langs,
                formats = formats
                ),
            DirectoryUpload(
                slavesrc="tmp",
                masterdest=Interpolate(
                    "/srv/buildbot/docs-site/www_content/%(kw:guide)s/%(src::branch)s", 
                    guide=guide 
                    ) 
                )
            ]
    return publican_factory_steps

def _publican_langtest_factory_step_generator(guide, lang, commit=False):
    anon_url, ssh_url = _guide_git_url(guide)
    todaystamp = datetime.now().utcnow().strftime("%Y-%m-%d")
    zanata_pull_command = [
            "/usr/bin/zanata",
            "--username immanetize",
            "--apikey {{  ansible_local.buildbot.pass.zanata_api_key }}",
            "--transdir ./%s./" % lang,
            "--lang %s" % lang
            ]
    today_stamp = datetime.now().utcnow().strftime("%Y-%m-%d")
    git_commit_command = [
            "/usr/bin/git",
            "commit",
            "-m",
            "docsbot %s translation update" % lang
            ]
    lang_integrator_steps = [
            Git(
                name = "%s ssh fetch" % guide,
                repourl=ssh_url,
                mode="full"
                ),
            ShellCommand(
                name = "zanata_pull",
                command = zanata_pull_command,
                haltOnFailure=True
                ),
            PublicanBuild(
                langs = ["en-US"],
                formats = ["html-single"]
                ),
            ShellCommand(
                name = "publican_clean",
                command = ["/usr/bin/publican", "clean"]
                )
            ]
    if commit:
        lang_integrator_steps.extend([
            ShellCommand(
                name = "prep_commit",
                command = ["/usr/bin/git", "add", "."]
                ),
            ShellCommand(
                name = "git_commit",
                command = git_commit_command
                ),
            ShellCommand(
                name = "push_commits",
                command = "git push"
                )
            ])
    return lang_integrator_steps

from buildbot.config import BuilderConfig

lan_buildslaves = []
{% for host in groups['buildbot-slaves'] %}
lan_buildslaves.append("{{ host }}")
{% endfor %}

all_publican_builders = [] 
all_translation_builders = {}
c['schedulers'] = []
#c['schedulers'].append(SingleBranchScheduler(
#                            name="all",
#                            change_filter=ChangeFilter(branch='master'),
#                            treeStableTimer=None,
#                            builderNames=["PublicanAllFormats"]))
#c['schedulers'].append(ForceScheduler(
#                            name="force",
#                            builderNames=["PublicanAllFormats"]))


c['builders'] = []
publican_factory = {}
for guide in guide_list:
    guide_publisher = "%s-publisher" % guide
    all_publican_builders.append(guide_publisher)
    publican_factory[guide_publisher]=BuildFactory(_publican_publisher_factory_step_generator(guide))
    c['builders'].append(
        BuilderConfig(
            name=guide_publisher,
            slavenames=lan_buildslaves,
            factory=publican_factory[guide_publisher]
            )
        )
    c['schedulers'].append(AnyBranchScheduler(
        name="%s_scheduler" % guide_publisher,
        builderNames=[guide_publisher],
        change_filter=filtered_branches,
        treeStableTimer=None
        ))
    c['schedulers'].append(SingleBranchScheduler(
        name="%s_master-scheduler" % guide_publisher,
        change_filter=ChangeFilter(branch='master'),
        builderNames=[guide_publisher],
        treeStableTimer=None,
        ))
    for lang in translated_langs:
        lang_tester = "%s_%s_translator" % (guide, lang)
        all_translation_builders.setdefault(lang, []).append(lang_tester)
        publican_factory[lang_tester] = BuildFactory(
                _publican_publisher_factory_step_generator(
                    guide, 
                    langs=[lang], 
                    formats=["html-single"]
                    )
                )
        c['builders'].append(
                BuilderConfig(
                    name = lang_tester,
                    slavenames=lan_buildslaves,
                    factory=publican_factory[lang_tester]
                    )
                )
        
        
for lang in translated_langs:
    for branch in published_branches:
        c['schedulers'].append(Nightly(
            name = "%s %s Translation Validator" % (branch, lang),
            branch = branch,
            builderNames = all_translation_builders[lang],
            hour = random.randint(2, 5),
            minute = random.randint(0,59)
            )
        )



    
c['schedulers'].append(ForceScheduler(
        name="PanicRebuild",
        builderNames=all_publican_builders
        ))

####### STATUS TARGETS

c['status'] = []

from buildbot.status import html
from buildbot.status.web import authz, auth

authz_cfg=authz.Authz(
    # change any of these to True to enable; see the manual for more
    # options
    auth=auth.BasicAuth([("pyflakes","pyflakes")]),
    gracefulShutdown = False,
    forceBuild = 'auth', # use this to test your slave once it is set up
    forceAllBuilds = 'auth',  # ..or this
    pingBuilder = False,
    stopBuild = False,
    stopAllBuilds = False,
    cancelPendingBuild = False,
)
c['status'].append(html.WebStatus(http_port=8010, authz=authz_cfg))

####### PROJECT IDENTITY

# the 'title' string will appear at the top of this buildbot
# installation's html.WebStatus home page (linked to the
# 'titleURL') and is embedded in the title of the waterfall HTML page.

c['title'] = "Fedora Docs Project Website Constructor"
c['titleURL'] = "https://docs.fedoraproject.org"
c['buildbotURL'] = "http://buildbot.home.randomuser.org:8010/"

####### DB URL

c['db'] = {
    # This specifies what database buildbot uses to store its state.  You can leave
    # this at its default for all but the largest installations.
    'db_url' : "sqlite:///state.sqlite",
}
