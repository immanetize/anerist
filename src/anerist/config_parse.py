# misc reqs
from copy import deepcopy
from buildbot.process.properties import Interpolate
# load_yaml reqs
import yaml
# change_source reqs
from buildbot.changes.gitpoller import GitPoller
from random import randint
# factory reqs
from buildbot.process.factory import BuildFactory
from buildbot.steps.source.git import Git
from buildbot.steps.shell import ShellCommand
from buildbot.steps.transfer import DirectoryUpload
from anerist.buildsteps import *
from os import path
from anerist.helpers import PublicanHelpers


class FactoryBuilder():
    jeff = PublicanHelpers()
    all_langs = jeff.valid_langs()
    def load_yaml(self, filename)
        """
        Give this a filename, and it returns a python object. 
        It does nothing else.
        """
        y  = open(filename)
        projects = yaml.load(y)
        y.close()
        return projects
    def project_processor(self, projects):
        """
        The python object returned by `load_yaml` is a list, and could 
        theoretically contain multiple projects.  This module walks through
        the requisite steps to create changesources, build factories, and
        schedulers for each project.
        """
        for project in projects:
            project['slug'] = project['name'].lower().replace(' ', '_')
            project['_prepped_change_sources'] = self.prep_change_source(project)
            for job in project['jobs']:
                project['_prepped_factories'][job['name']] = self.prep_factory(project, job)


    def prep_factory(self, project, job):
        """
        Creates a build factory for a given job in a project.  Each job should
        have one or more declared steps.

        Each step should declare one of a set of predefined `types`:

        scm_pull:
            Uses the project's `scm_type` and `source_uri` to create a job to
            refresh the local content repository.

        translation_pull, translation push:
            Uses the project's `translation_type` and `translation_uri` to
            create a job that interacts with a translation method or 
            service.

            The job expects a list of languages to pull, or a single language 
            code, but can also accept some special values:

            - all: attempt to pull strings for all language codes known to the
              project's document type.

            - native_language:  Use the project's declared native language.

            - +50% (any percentage will do):  Pull translations with over N%
              string completion.  I expect this value will be interpolated
              when the service starts up, not at the time the job is run, 
              so use this method with caution for now.

            Translation jobs that interact with an external service may also 
            expect user credentials for that service are available in a local 
            file.  For example, the `zanata` client expects 
            `~/.config/zanata.ini`.  A step is automatically added to relevant
            jobs to check for the file and halt on failure to find it.
        """
        steps = []
        for step in job['steps']:
            # we allowed some simplicity in the config file's language declaration, 
            # and have to make up for it here.
            if not step['langs']:
                step['langs'] == [ project['native_language'] ]
            if step['langs'] == 'all':
                step['langs']  = self.all_langs
            if step['langs'] == 'native_language':
                step['langs'] == [ project['native_language'] ]
            if isinstance(step['langs'], basestring):
                step['langs'] = [ step['langs'] ]
            if step['type'] == 'scm_pull':
                if project['scm_type'] == 'git':
                    steps.append(
                            Git(
                                name = "fetch %s sources" % project['name'],
                                repourl = project['source_uri'],
                                mode = 'full',
                                method = 'clean',
                                haltOnFailure = 'true'
                                description = job['name']
                                descriptionDone = "%s done" % job['name']
                                )
                else:
                    print('Sorry, only "git" fetches are currently supported.')
            if step['type'] in ['translation_push', 'translation_pull']:
                    if project['translation_type'] == 'zanata':
                        steps.append(
                            ShellCommand(
                                name = 'check for Zanata credentials'
                                description = 'i10n cred file check'
                                descriptionDone = 'creds ok'
                                command = [
                                    "test", 
                                    "-f",
                                    "%s/config/zanata.ini" % path.expanduser('~')
                                    ]
                                )
                    else:
                        print('Sorry, only Zanata translation is currently supported.')


        factory = BuildFactory(steps)
        return factory
    def prep_change_source(self, project):
        change_sources = []
        if project['scm_type'] == 'git':
            change_sources.append(
                    GitPoller(
                        project['source_uri'],
                        workdir = project['slug'],
                        branches = True,
                        pollinterval = randint(30, 120)
                        categoy = 'git_watcher'
                        )
                    )
        else:
            print('Sorry, only "git" poller change sources are currently supported.')
        return change_sources

    def scheduler_generator(self, project)




