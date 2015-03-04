# -*- python -*-
# ex: set syntax=python:

# This is a sample buildmaster config file. It must be installed as
# 'master.cfg' in your buildmaster's base directory.

# This is the dictionary that the buildmaster pays attention to. We also use
# a shorter alias to save typing.
c = BuildmasterConfig = {}

####### BUILDSLAVES

# The 'slaves' list defines the set of recognized buildslaves. Each element is
# a BuildSlave object, specifying a unique slave name and password.  The same
# slave name and password must be configured on the slave.
from buildbot.buildslave import BuildSlave
c['slaves'] = [
	BuildSlave("buildslave01.home.randomuser.org", "{{ ansible_local.buildbot.pass.buildslave_pass }}"),
	BuildSlave("buildslave02.home.randomuser.org", "{{ ansible_local.buildbot.pass.buildslave_pass }}"),
	BuildSlave("buildslave03.home.randomuser.org", "{{ ansible_local.buildbot.pass.buildslave_pass }}"),
	]

# 'protocols' contains information about protocols which master will use for
# communicating with slaves.
# You must define at least 'port' option that slaves could connect to your master
# with this protocol.
# 'port' must match the value configured into the buildslaves (with their
# --master option)
c['protocols'] = {'pb': {'port': 9989}}

latest_release = 22
oldest_release = 19
release_range = range(oldest_release, latest_release)
published_branches = []
for release in release_range:
    published_branches.append("f%s" % release)
    published_branches.append("F%s" % release)

language_list = [
        "ar-SA",
        "as-IN",
        "ast-ES",
        "bn-IN",
        "bs-BA",
        "bg-BG",
        "ca-ES",
        "zh-CN",
        "zh-HK",
        "zh-TW",
        "cs-CZ",
        "da-DK",
        "fi-FI",
        "fr-FR",
        "de-DE",
        "el-GR",
        "gu-IN",
        "he-IL",
        "hi-IN",
        "hr-HR",
        "hu-HU",
        "id-ID",
        "ia",
        "is-IS",
        "it-IT",
        "ja-JP",
        "kn-IN",
        "ko-KR",
        "lv-LT",
        "lv-LV",
        "ml-IN",
        "mr-IN",
        "nb-NO",
        "nl-NL",
        "or-IN",
        "pa-IN",
        "fa-IR",
        "pl-PL",
        "pt-PT",
        "pt-BR",
        "ro-RO",
        "ru-RU",
        "sr-RS",
        "sr-Latn-RS",
        "si-LK",
        "sk-SK",
        "es-ES",
        "sv-SE",
        "ta-IN",
        "te-IN",
        "uk-UA",
        "de-CH",
        "th-TH"
        ]

guide_list = [
	"accessibility-guide",
	"amateur-radio-guide",
	"anaconda-addon-development-guide",
	"ARM-getting-started-guide",
	"cloud-guide",
	"deployment-guide",
	"docs-beginner",
	"docsite-publican",
	"documentation-guide",
	"elections-guide",
	"fedora-cookbook",
	"fedora-server-guide",
	"firewall-guide",
	"freeipa-guide",
	"installation-quick-start-guide",
	"install-guide",
	"multiboot-guide",
	"musicians-guide",
	"networking-guide",
	"openssh-guide",
	"packagers-guide",
	"power-management-guide",
	"readme-burning-isos",
	"release-notes",
	"resource-management-guide",
	"respin-guide",
	"robotics-guide",
	"rpm-guide",
	"secure-ruby-development-guide",
	"securityguide",
	"selinux-guide",
	"selinux-user-guide",
	"software-collections-guide",
	"software-management-guide",
	"storage-administration-guide",
	"system-administrators-guide",
	"system-administrators-reference-guide",
	"technical-notes",
	"translation-quick-start-guide",
	"uefi-secure-boot-guide",
	"user-guide",
	"virtualization-administration-guide",
	"virtualization-deployment-and-administration-guide",
	"virtualization-deployment-guide",
	"virtualization-getting-started-guide",
	"virtualization-guide",
	"virtualization-security-guide",
	"writers-style-guide",
]

def _guide_git_url(guide):
    anon_url = "https://git.fedorahosted.org/git/docs/%s.git" % guide
#    ssh_url = "ssh://git.fedorahosted.org/git/docs/%s.git" % guide
    ssh_url = "ssh://buildbot@lemuria.home.randomuser.org:/srv/projects/docs/guides/%s" % guide
    return anon_url, ssh_url
  
####### CHANGESOURCES

# the 'change_source' setting tells the buildmaster how it should find out
# about source code changes.  Here we point to the buildbot clone of pyflakes.

from buildbot.changes.gitpoller import GitPoller
import random

c['change_source'] = []

for guide in guide_list:
    anon_url, ssh_url = _guide_git_url(guide)
    c['change_source'].append(GitPoller(
        anon_url, 
        workdir=guide, 
        branches=published_branches.append("master"),
        pollinterval=random.randint(300,600)
        ))

####### SCHEDULERS

# Configure the Schedulers, which decide how to react to incoming changes.  In this
# case, just kick off a 'runtests' build

from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.schedulers.forcesched import ForceScheduler
from buildbot.changes.filter import ChangeFilter
from buildbot.scheduler import Nightly

filtered_branches = ChangeFilter(
        branch_fn = published_branches
        )


####### BUILDERS

# The 'builders' list defines the Builders, which tell Buildbot how to perform a build:
# what steps, and which slaves can execute them.  Note that any particular build will
# only take place on one slave.

from buildbot.process.factory import BuildFactory
from buildbot.steps.source.git import Git
from buildbot.steps.shell import ShellCommand
from buildbot.process.factory import Publican
from buildbot.steps.transfer import DirectoryUpload
from buildbot.process.properties import Interpolate
from datetime import datetime

def _publican_publisher_factory_step_generator(guide):
    anon_url, ssh_url = _guide_git_url(guide)
    publican_factory_steps = [
            Git(
                name = "%s fetch" % guide,
                repourl=anon_url,
                mode='incremental'
                ),
            ShellCommand(
                name = "%s build" % guide,
                command=["publican", "build", "--langs=all", "--formats=html,html-single,pdf,epub"],
                haltOnFailure=True
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

def _publican_langtest_factory_step_generator(guide, lang):
    anon_url, ssh_url = _guide_git_url(guide)
    todaystamp = datetime.now().utcnow().strftime("%Y-%m-%d")
    zanata_pull_command = [
            "/usr/bin/zanata",
            "--username immanetize",
            "--apikey 14383a7c8ccc3126c1622c50c0978410",
            "--transdir ./%s./" % lang,
            "--lang %s" % lang
            ]
    today_stamp = datetime.now().utcnow().strftime("%Y-%m-%d")
    publican_build_command = [
            "/usr/bin/publican",
            "build",
            "--langs %s" % lang,
            "--formats html"
            ]
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
            ShellCommand(
                name = "test_%s_build" % lang,
                command = publican_build_command,
                haltOnFailure=True
                ),
            ShellCommand(
                name = "publican_clean",
                command = ["/usr/bin/publican", "clean"]
                ),
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
            ]
    return lang_integrator_steps

from buildbot.config import BuilderConfig

lan_buildslaves = [
        "buildslave01.home.randomuser.org",
  	    "buildslave02.home.randomuser.org",
        "buildslave03.home.randomuser.org"
        ]

all_publican_builders = []

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

    
for guide in ["release-notes"]:
    for lang in language_list:
        publican_lang_test_builder = "%s-%s-integrator" % (guide, lang)
        publican_factory[publican_lang_test_builder]=BuildFactory(
                _publican_langtest_factory_step_generator(guide, lang)
                )
        c['builders'].append(
                BuilderConfig(
                    name=publican_lang_test_builder,
                    slavenames=lan_buildslaves,
                    factory=publican_factory[publican_lang_test_builder]
                    )
                )
        c['schedulers'].append(AnyBranchScheduler(
                name=publican_lang_test_builder,
                builderNames=[publican_lang_test_builder],
                change_filter=filtered_branches,
                treeStableTimer=None
                )
            )
                       

c['schedulers'].append(ForceScheduler(
                            name="PanicRebuild",
                            builderNames=all_publican_builders
                            ))

####### STATUS TARGETS

# 'status' is a list of Status Targets. The results of each build will be
# pushed to these targets. buildbot/status/*.py has a variety to choose from,
# including web pages, email senders, and IRC bots.

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

# the 'buildbotURL' string should point to the location where the buildbot's
# internal web server (usually the html.WebStatus page) is visible. This
# typically uses the port number set in the Waterfall 'status' entry, but
# with an externally-visible host name which the buildbot cannot figure out
# without some help.

c['buildbotURL'] = "http://buildbot.home.randomuser.org:8010/"

####### DB URL

c['db'] = {
    # This specifies what database buildbot uses to store its state.  You can leave
    # this at its default for all but the largest installations.
    'db_url' : "sqlite:///state.sqlite",
}