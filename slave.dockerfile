FROM fedora:22
MAINTAINER https://github.com/immanetize/anerist

RUN dnf update -y && dnf clean all
RUN dnf install python-beautifulsoup4 PyYaml python-setuptools packagedb-cli GitPython git buildbot-slave zanata-python-client publican publican-fedora && dnf clean all

RUN mkdir -p /srv/buildbot

ADD ./anerist /srv/anerist
RUN cd /srv/anerist && python setup.py develop

RUN buildbot create-slave -r /srv/buildbot/anerist-slave localhost:9989 Lift&Mid6Glee

WORKDIR /srv/buildbot/anerist-slave 
CMD buildslave start
