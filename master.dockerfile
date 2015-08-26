FROM fedora:22
MAINTAINER https://github.com/immanetize/anerist

RUN dnf clean all && dnf update -y --setopt="deltarpm=0" 
RUN dnf install -y python-beautifulsoup4 PyYAML python-setuptools packagedb-cli GitPython git buildbot-master  zanata-python-client publican publican-fedora

RUN mkdir -p /srv/buildbot

COPY ./anerist /srv/anerist
RUN cd /srv/anerist && python setup.py develop

RUN buildbot create-master -r /srv/buildbot/anerist
COPY ./resources/buildbot/master.py /srv/buildbot/anerist/

EXPOSE 8010
EXPOSE 9989

WORKDIR /srv/buildbot/anerist 
CMD buildbot start
