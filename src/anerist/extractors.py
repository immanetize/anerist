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
    """
    Give it a string, and slugify makes it a slug. Spaces are converted to
    hyphens, some basic language processing is done - for now, removing 
    articles - and all characters are lower-cased.
    """
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
    """
    This simply helps ConfigParser read perl config::simple config files.
    """
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
    """
    Extracts metadata from a ReStructuredText document.  Some 'custom' directives are
    expected, refer to rst/custom_directives for details.
    """
    parser = rst.Parser(rfc2822=True)

    def _read_rst_config(self, contents, source_path=None, destination_path=None):
        """
        Pass in a ReStructuredText document, as a string, and get back a docutils
        document object.
        """
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
        """
        Give an entire ReStructuredText document, as a docutils 'document' object.
        Returns specific, targeted document attributes.
        Use like:
            title, slug, abstract, tags, taxonomy = _parse_metadata(document)
        """
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
        """
        Give a path to a ReStructuredText file, receive the file's metadata.
        """
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
        """
        Give it a list of files or paths, and it does all the things
        to retrieve metadata from ReStructuredText files it finds.

        The read_broker expects three arguments:

        - target: a list of files or paths to search.  Given paths,
            looks only for files ending in ".rst"
        
        - lang: The language code of the target document.  Usefulness is
            dubious here.

        - extra_args: A dictionary of extra metadata to slap on after 
            reading the file.

        """
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
    """
    Extracts metadata from a docbook project.  A few assumptions are made:

    - XML files for a given language are stored in a folder named by the language code.
      For example, US English sources are stored in an en-US directory.  

    - This does not currently interpolate translation strings.  It expects fully prepared
      sources in the target language.

    - Content is mostly or wholly derived from either Book_Info.xml or Article_Info.xml.

    - Document taxonomy is represented in a <subjectterm> value.

    - Document tags are represented in a <keywordset> set.

    The first three asumptions are met with any publican-created projects.  
    Other docbook source paradigms will need to have support added in the future.
    """
    def _get_xml_filelists(self, target, lang, scope='all'):
        """
        Given a list of paths, this walks the paths and returns a list of
        XML files, and a list of XML entity files, that are discovered there.
        
        It isn't smart, filename will need to end with ".xml" or ".ent", respectively.
        This could probably be improved with mime type detection, or whatever
        /usr/bin/file does.  It doesn't know about entities within XML files; the 
        entity files are presumed to be in a format like::

            <!ENTITY PRODUCT "Anerist">
            <!ENTITY BOOKID "Anerist Guide">

        """

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
        """
        Given a list of xml files, this finds either Book_Info.xml or Article_Info.xml
        and returns their content as a string.

        This could be improved by finding the actual <bookinfo> or <articleinfo> tag set,
        even if those files aren't available.
        """
        pub_types = "Book", "Article"
        for name in xml_files:
            if os.path.basename(name).endswith("Info.xml") and os.path.basename(name).startswith(pub_types): #&& if info_file is not set?
                info_file = name
        xml = open(info_file)
        xml_string = unicode(xml.read())
        xml.close()
        return xml_string
        


    def _substitute_entities(self, xml_string, entity_dict):
        """
        Give it an XML string that potentially contains entities, and a dictionary
        of entity values, and it interpolates the entity values and returns the
        processed string. 
        """
        for item in entity_dict.keys():
            xml_string = re.sub('&%s;' % item, entity_dict[item], xml_string)
        return xml_string
        
    def _get_entity_dict(self, entity_filelist):
        """
        Takes a list of files containing entity declarations, and returns a dictionary
        containing entity names and their values.
        """
        
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

        # add some known values
        entity_dict['nbsp'] = " "
        entity_dict['amp'] = "&"
        return entity_dict

    def _get_docbook_metadata(self, interpolated_xml_string, lang, extra_args):
        """
        Returns a dictionary of document metadata from an XML string.  This presumes some
        tags are present:

        - <title>
        - <abstract>
        - <keywordset>, with <keyword> children
        - <subjectset>, with a single <subjectterm> child

        Improperly prepared sources will probably fail.
        """
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
        """
        Given a list of paths, this does all the things and returns a
        python object with their metadata.
        """
        entity_filelist, xml_filelist = self._get_xml_filelists(target, lang)
        info = self._get_xmldoc_info(xml_filelist)
        entity_dict = self._get_entity_dict(entity_filelist)
        interpolated_xml = self._substitute_entities(info, entity_dict)
        meta = self._get_docbook_metadata(interpolated_xml, lang, extra_args)
        return meta
