#!/usr/bin/python
# Extract metadata from a publican book
import argparse
import os
import re
import ConfigParser
from bs4 import BeautifulSoup
import yaml
import json
from docutils import core, io

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
class meta_handler():
    def _read_rst_config(self, docfile, source_path=None, destination_path=None):
        f = open(docfile, 'r')
        doc_string = unicode(f.read())
        f.close()
        overrides = {}
        overrides['input_encoding'] = 'unicode'
        output, pub = core.publish_programmatically(
            source_class=io.StringInput, 
            source=doc_string,
            source_path=source_path,
            destination_class=io.NullOutput, destination=None,
            destination_path=destination_path,
            reader=None, reader_name='standalone',
            parser=None, parser_name='restructuredtext',
            writer=None, writer_name='null',
            settings=None, settings_spec=None, settings_overrides=overrides,
            config_section=None, enable_exit_status=None
            )
        return output, pub 

    def _get_xml_filelists(self, path=os.getcwd(), lang="en-US", scope='all'):
        xml_files = []
        entity_files = []
        for root, dirs, files in os.walk(path, lang):
            for name in files:
                if name.endswith("xml"):
                    xml_files.append(os.path.join(root, name)
                else if name.endswith("ent"):
                    entity_files.append(os.path.join(root, name)
        if scope is 'all':
            return xml_files, entity_files
         #placeholder - maybe later we might only want xml or entities
      

    def _read_publican_config(self, configfile='publican.cfg', lang='en-US'):
        pcfg = ConfigParser.SafeConfigParser()
        pcfg.readfp(FakeSecHead(open(configfile)))
        book_type = pcfg.get('pants', 'type')
        document_root = os.path.dirname(configfile)
        info_file = "%s/%s/%s_Info.xml" % (
                document_root,
                lang, 
                book_type
                )
        entity_file = "%s/%s/%s.ent" % (
                os.path.dirname(configfile),
                lang, 
                book_type
                )

        info = open(info_file)
        docsoup = BeautifulSoup(info)
        title = docsoup.title.string
        stub = docsoup.subtitle.string
        abstract = docsoup.abstract.para.string
        for root, dirs, files in os.walk("%s/%s" % (document_root, lang)):
            for name in files:
                if name.endswith('ent'):
                    entity_file = os.path.join(root, name)
        entity_list = []
        ent = {}
        entity_list.extend(open(entity_file))
        for line in entity_list:
            entlist = line.split()
            if len(entlist):
                ent_str = " ".join(entlist[2:])
                ent[entlist[1]] = ent_str.strip('"')
        for entity in ent:
            ent[entity] = re.sub('>$', '', ent[entity])
        for item in ent:
            for value in ent:
                ent[value] = re.sub('&%s;' % item, ent[item], ent[value])
        for item in ent:
            title = re.sub('&%s;' % item, ent[item], title)
            stub = re.sub('&%s;' % item, ent[item], stub)
            abstract = re.sub('&%s;' % item, ent[item], abstract)
        return title, stub, abstract

    def _write_json(self, meta, metadata="metadata.json"):
        f = open(metadata, 'w')
        attributes = {
            "title":    meta['title'],
            "stub":     meta['stub'],
            "abstract": meta['abstract']
            }
        printable_json = json.dumps(attributes, encoding="utf-8", indent=3)
        f.write(printable_json)
        f.close()

    def _load_json(self, metadata="metadata.json"):
        f = open(metadata, 'r')
        meta = json.loads(f.read())
        return meta

    def _load_yaml(self, metadata="metadata.yml"):
        y = open(metadata)
        meta = yaml.load(y)
        y.close()
        return meta

    def _write_yaml(self, meta, metadata="metadata.yml"):
        y = open('metadata.yml', 'w')
        yaml.dump(meta, y, default_flow_style=False)
        y.close()

