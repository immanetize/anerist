import argparse
import os
import re
import ConfigParser
from bs4 import BeautifulSoup
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
                document.pop(document.index(element))
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
    def _read_file(self, inputfile, lang, extra_args):
        output = {}
        f = open(inputfile, 'r')
        print("reading " + os.path.basename(inputfile))
        contents = unicode(f.read(), errors='replace')
        f.close()
        document = self._read_rst_config(contents)
        output['title'], output['slug'], output['abstract'], output['tags'], output['taxonomy'] = self._parse_metadata(document)
        output['source_type'] = "rest"
        output['lang'] = lang
        if extra_args:
            for key in extra_args.keys():
                output[key] = extra_args[key]
        return output
    def read_broker(self, target, lang, extra_args):
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
            metadatum = self._read_file(inputfile, lang, extra_args)
            metadata.append(metadatum)
        
        return metadata

class docbook():
    def _get_xml_filelists(self, target, lang, scope='all'):
        xml_files = []
        entity_files = []
        for item in target:
#            item = unicode(item, errors='replace')
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
        


    def _substitute_entities(self, xml_string, entity_dict):
        for item in entity_dict.keys():
            xml_string = re.sub('&%s;' % item, entity_dict[item], xml_string)
        return xml_string
        
    def _get_entity_dict(self, entity_filelist):
        def remove_member(l, member):
            if member in l:
                l.remove(member)
            return l
        entity_dict = {}
        for entity_file in entity_filelist:
            f = open(entity_file)
            e = unicode(f.read())
            e = re.sub('\n', ' ', e)
            for ee in remove_member(e.split('ENTITY'), '<!'):
                ll = remove_member(ee.split(), '<!')
                entity_name = ll[0]
                entity_value = re.sub('>$', '', ' '.join(ll[1:]))
                entity_dict[entity_name] = entity_value
        for item in entity_dict.keys():
            for value in entity_dict.keys():
                entity_dict[item] = re.sub('&%s;' % value, entity_dict[value], entity_dict[item])

        return entity_dict

    def _get_docbook_metadata(self, interpolated_xml_string, lang, extra_args):
        docsoup = BeautifulSoup(interpolated_xml_string, "lxml")
        metadata = []
        output = {}
        # TODO: error handling for books without the desired attributes
        output['title'] = docsoup.title.string
        output['slug'] = slugify(docsoup.title.string)
        output['abstract'] = docsoup.subtitle.string
        output['taxonomy'] = docsoup.subjectterm.string
        output['source_type'] = 'docbook'
        output['lang'] = lang
        output['tags'] = []
        for tag in docsoup.keywordset.findChildren():
            output['tags'].append(tag.string)
        if extra_args:
            for key in extra_args.keys():
                output[key] = extra_args[key]
        metadata.append(output)
        return metadata

    def read_broker(self, target, lang, extra_args):
        entity_filelist, xml_filelist = self._get_xml_filelists(target, lang)
        info = self._get_xmldoc_info(xml_filelist)
        entity_dict = self._get_entity_dict(entity_filelist)
        interpolated_xml = self._substitute_entities(info, entity_dict)
        meta = self._get_docbook_metadata(interpolated_xml, lang, extra_args)
        return meta
