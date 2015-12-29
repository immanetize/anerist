# misc reqs
from copy import deepcopy
# load_yaml reqs
import yaml
# change_source reqs
from buildbot.changes.gitpoller import GitPoller
from random import randint

class FactoryBuilder():
    def load_yaml(self, filename)
        y  = open(filename)
        projects = yaml.load(y)
        y.close()
        return projects
    def project_processor(self, projects):
        for project in projects:
            project['slug'] = project['name'].lower().replace(' ', '_')
            project['_prepped_change_sources'] = self.prep_change_source(project)

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

    def factory_generator(self, job):

    def scheduler_generator(self, 




