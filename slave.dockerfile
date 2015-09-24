FROM fedora:22
MAINTAINER https://github.com/immanetize/anerist

RUN dnf update -y && dnf clean all
RUN dnf install -y python-beautifulsoup4 PyYAML python-setuptools packagedb-cli GitPython git zanata-python-client publican publican-fedora dnf-plugins-core && dnf clean all
RUN dnf copr enable immanetize/buildbot-nine && dnf install -y buildbot buildbot-slave && dnf clean all

RUN mkdir -p /srv/buildbot

ADD ./src /srv/anerist
RUN cd /srv/anerist && python setup.py develop

RUN buildslave create-slave -r /srv/buildbot/anerist-slave anerist-master:9989 anerist-slave 'Lift&Mid6Glee'

WORKDIR /srv/buildbot/anerist-slave 
CMD buildslave start && tail -f twistd.log
