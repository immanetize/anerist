#!/usr/bin/python
# Extract metadata from a publican book
from docutils.parsers import rst
from docutils.nodes import Special, Invisible, FixedTextElement

class slug(Special, Invisible, FixedTextElement):
    pass

class Slug(rst.Directive):
    required_arguments = 1
    optional_argumetns = 0
    has_conent = True
    def run(self):
        thenode = slug(text=self.arguments[0])
        return [thenode]

rst.directives.register_directive('slug', Slug)


