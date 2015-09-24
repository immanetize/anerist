FROM fedora
MAINTAINER https://github.com/immanetize/anerist

RUN dnf update -y --setopt="deltarpm=0" && dnf clean all
RUN dnf install -y python-beautifulsoup4 PyYAML python-setuptools packagedb-cli GitPython git zanata-python-client publican publican-fedora dnf-plugins-core && dnf clean all
RUN dnf copr enable immanetize/buildbot-nine -y && dnf install -y buildbot-master && dnf clean all
RUN mkdir -p /srv/buildbot

ADD src /srv/anerist
RUN cd /srv/anerist && python setup.py develop

RUN buildbot create-master -r /srv/buildbot/anerist
ADD ./resources/buildbot/master.py /srv/buildbot/anerist/master.cfg

EXPOSE 8010
EXPOSE 9989

WORKDIR /srv/buildbot/anerist 
CMD buildbot start || tail -f twistd.log
