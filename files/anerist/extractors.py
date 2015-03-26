#!/usr/bin/python



# Extract metadata from a publican book
import os
import ConfigParser
from bs4 import BeautifulSoup
import yaml

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

def _read_publican_config(configfile, lang='en-US'):
    pcfg = ConfigParser.SafeConfigParser()
    pcfg.readfp(FakeSecHead(open(configfile)))
    book_type = pcfg.get('pants', 'type')
    info_file = "%s/%s_Info.xml" % (lang, book_type)
    info = open(info_file)

    docsoup = BeautifulSoup(info)

    title = docsoup.title.string
    stub = docsoup.subtitle.string
    abstract = docsoup.abstract.para.string

    for root, dirs, files in os.walk(lang):
        for name in files:
            if name.endswith('ent'):
                entity_file = os.path.join(root, name)

    entity_list = []
    ent = {}
    entity_list.extend(open(entity_file))

    for line in entity_list:
        entlist = line.split()
        if len(entlist):
            ent[entlist[1]] = " ".join(entlist[2:].strip('"')
                
    for item in ent:
        ent[item] = re.sub('>$', '', ent[item])
    for item in ent:
        for value in ent:
            ent[value] = re.sub('&%s;' % item, ent[item], ent[value])

    for item in ent:
        title = re.sub('&%s;' % item, ent[item], title)
        stub = re.sub('&%s;' % item, ent[item], stub)
        abstract = re.sub('&%s;' % item, ent[item], abstract)

    return title, stub, abstract        
y = open('metadata.yml')
meta = yaml.load(y)
y.close()

# do stuff to meta
y = open('metadata.yml', 'w')
yaml.dump(meta, y, default_flow_style=False)
y.close()

