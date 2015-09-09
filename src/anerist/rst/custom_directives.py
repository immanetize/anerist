#!/usr/bin/python
# Extract metadata from a publican book
from docutils.parsers import rst
from docutils.nodes import Special, Invisible, FixedTextElement

class slug(Special, Invisible, FixedTextElement):
    pass

class Slug(rst.Directive):
    required_arguments = 1
    optional_argumetns = 0
    has_content = True
    def run(self):
        thenode = slug(text=self.arguments[0])
        return [thenode]

rst.directives.register_directive('slug', Slug)


class tags(Special, Invisible, FixedTextElement):
    pass

class Tags(rst.Directive):
    required_arguments = 1
    optional_argumetns = 0
    has_content = True
    final_argument_whitespace = True
    def run(self):
        thenode = tags(text=self.arguments[0])
        return [thenode]

rst.directives.register_directive('tags', Tags)

class abstract(Special, Invisible, FixedTextElement):
    pass

class Abstract(rst.Directive):
    required_arguments = 1
    optional_argumetns = 0
    has_content = True
    final_argument_whitespace = True
    def run(self):
        thenode = abstract(text=self.arguments[0])
        return [thenode]

rst.directives.register_directive('abstract', Abstract)

class taxonomy(Special, Invisible, FixedTextElement):
    pass

class Taxonomy(rst.Directive):
    required_arguments = 1
    optional_argumetns = 0
    has_content = True
    final_argument_whitespace = False
    def run(self):
        thenode = taxonomy(text=self.arguments[0])
        return [thenode]

rst.directives.register_directive('taxonomy', Taxonomy)
