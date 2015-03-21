#!/usr/bin/python

# Extract metadata from a publican book

import ConfigParser
from bs4 import BeautifulSoup


configfile = 'publican.cfg'

# Thanks Alex Martelli!
# https://stackoverflow.com/questions/2819696/parsing-properties-file-in-python/2819788#2819788
class FakeSecHead(object):
    def __init__(self, fp):
        self.fp = fp
        self.sechead = '[pants]\n'

    def readline(self):
        if self.sechead:
            try: 
                return self.sechead
            finally: 
                self.sechead = None
        else: 
            return self.fp.readline()

pcfg = ConfigParser.SafeConfigParser()
pcfg.readfp(FakeSecHead(open(configfile)))
booktype = pcfg.get('pants', 'type')
info_file = "en-US/%s_Info.xml" % book_type
info = open(info_file)

docsoup = BeautifulSoup(info)

headline = docsoup.title.string
dope = docsoup.abstract.para.string
kicker = docsoup.subtitle.string

for root, dirs, files in os.walk('en-US'):
    for name in files:
        if name.endswith('ent'):
            print os.path.join(root, name)

