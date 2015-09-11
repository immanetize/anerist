#!/usr/bin/python
# Extract metadata from a publican book
import argparse
import os
import re
import ConfigParser
from bs4 import BeautifulSoup
import yaml
import json
from docutils import core, io, nodes
from docutils.parsers import rst
from docutils.nodes import Special, Invisible, FixedTextElement
from anerist.rst import custom_directives

def slugify(title):
    title = title.lower()
    words = title.split(' ')
    articles = "a", "an", "the"
    words_removed = 0
    for word in words:
        if word in articles:
            words.remove(word)
    title = '-'.join(words)
    return title


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
class rest():
    parser = rst.Parser(rfc2822=True)

    def _read_rst_config(self, contents, source_path=None, destination_path=None):
        overrides = {}
        overrides['input_encoding'] = 'unicode'
        output, pub = core.publish_programmatically(
            source_class=io.StringInput, 
            source=contents,
            source_path=source_path,
            destination_class=io.NullOutput, destination=None,
            destination_path=destination_path,
            reader=None, reader_name='standalone',
            parser=self.parser, parser_name='restructuredtext', #parser=None, parser_name='restructuredtext',
            writer=None, writer_name='null',
            settings=None, settings_spec=None, settings_overrides=overrides,
            config_section=None, enable_exit_status=None
            )
        document = pub.writer.document
        return document     
    def _parse_metadata(self, document):
        title = document.get('title')
        for element in document:
            if element.tagname == 'slug':
                slug = element.astext()
                # we don't have anything to reder this, so get it out!
                doc.pop(doc.index(element))
            elif element.tagname is 'abstract':
                abstract = element.astext()
            elif element.tagname is 'tags':
                tags = element.astext().split(',')
            elif element.tagname is 'taxonomy':
                taxonomy = element.astext()
            elif element.tagname is 'title':
                explicit_title = element.astext()
        if not 'abstract' in locals():
            abstract = ""
        if not 'tags' in locals():
            tags = []
        if not 'taxonomy' in locals():
            taxonomy = "uncategorized"
        if 'explicit_title' in locals():
            title = explicit_title            
        if not 'slug' in locals():
            slug = slugify(title)
               
        return title, slug, abstract, tags, taxonomy
    def _read_file(self, inputfile, lang):
        output = {}
        f = open(inputfile, 'r')
        print("reading " + os.path.basename(inputfile))
        contents = unicode(f.read(), errors='replace')
        f.close()
        document = self._read_rst_config(contents)
        output['title'], output['slug'], output['abstract'], output['tags'], output['taxonomy'] = self._parse_metadata(document)
        output['source_type'] = "rest"
        output['lang'] = lang
        return output
    def read_broker(self, target, lang):
        metadata = []
        file_list = []
        for item in target:
            if os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    for name in files:
                        if name.endswith("rst"):
                            file_list.append(os.path.join(root, name))
            elif os.path.isfile(item) or os.path.islink(item):
                file_list.append(item)
            else:
                print("Invalid target type specified")
                sys.exit()
        for inputfile in file_list:
            metadatum = self._read_file(inputfile, lang)
            metadata.append(metadatum)
        return metadata

        

        
class docbook():
    # TODO: Move path default up the logic
    def _get_xml_filelists(self, target, lang, scope='all'):
        xml_files = []
        entity_files = []
        for item in target:
            item = unicode(item, errors='replace')
            for root, dirs, files in os.walk(item, lang):
                for name in files:
                    if name.endswith("xml"):
                        xml_files.append(os.path.join(root, name)) 
                    elif name.endswith("ent"):
                       entity_files.append(os.path.join(root, name))
        return entity_files, xml_files
         #placeholder - maybe later we might only want xml or entities
      
    def _get_xmldoc_info(self, xml_files):
        pub_types = "Book", "Article"
        for name in xml_files:
            if os.path.basename(name).endswith("Info.xml") and os.path.basename(name).startswith(pub_types): #&& if info_file is not set?
                info_file = name
        xml = open(info_file)
        xml_string = unicode(xml.read())
        xml.close()
        return xml_string
        


    def _substitute_entities(self, xml_string, entity_filelist):

        entity_list = []
        ent = {}
        for entity_file in entity_filelist:
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
            interpolated_xml = re.sub('&%s;' % item, ent[item], xml_string)
        return interpolated_xml

    def _get_docbook_metadata(self, interpolated_xml_string):
        docsoup = BeautifulSoup(interpolated_xml_string, "lxml")
        metadata = []
        output = {}
        output['title'] = docsoup.title.string
        output['slug'] = slugify(docsoup.title.string)
        output['abstract'] = docsoup.subtitle.string
        output['source_type'] = 'docbook'
        output['lang'] = lang
        output['tags'] = []
        metadata.append(output)
        return metadata

    def read_broker(self, target, lang):
        entity_filelist, xml_filelist = self._get_xml_filelists(target, lang)
        info = self._get_xmldoc_info(xml_filelist)
        interpolated_xml = self._substitute_entities(info, entity_filelist)
        meta = self._get_docbook_metadata(interpolated_xml, lang)
        return meta

class file_handlers():
    def write_json(self, meta, output="metadata.json"):
        f = open(output, 'w')
        printable_json = json.dumps(meta, encoding="utf-8", indent=3)
        f.write(printable_json)
        f.close()

    def load_json(self, metadata="metadata.json"):
        f = open(metadata, 'r')
        meta = json.loads(f.read())
        return meta

    def load_yaml(self, metadata="metadata.yml"):
        y = open(metadata)
        meta = yaml.load(y)
        y.close()
        return meta

    def write_yaml(self, meta, metadata="metadata.yml"):
        y = open('metadata.yml', 'w')
        yaml.dump(meta, y, default_flow_style=False)
        y.close()

