#!/usr/bin/python
# Extract metadata from a publican book
from docutils.parsers import rst
from docutils.nodes import Special, Invisible, FixedTextElement

class slug(Special, Invisible, FixedTextElement):
    """Directive type declaration for the 'slug' directive."""
    pass

class Slug(rst.Directive):
    """
    Defines a 'slug' docutils node for metadata processing.
    This is intended to be used for cross-document links and
    human-readable URLs. Catches things defined like this:

       .. slug:: your-slug-here

    Content is not rendered.
    """
    required_arguments = 1
    optional_argumetns = 0
    has_content = True
    def run(self):
        thenode = slug(text=self.arguments[0])
        return [thenode]

rst.directives.register_directive('slug', Slug)


class tags(Special, Invisible, FixedTextElement):
    """Directive type declaration for the 'tags' directive."""
    pass

class Tags(rst.Directive):
    """
    Defines a 'tags' docutils node for metadata processing.
    It expects a terse comma-separated list of keywords 
    relevant to the document, and catches things defined 
    like this:

       .. tags:: lizard, potato, orangutan

    Content is not rendered.
    """
    required_arguments = 1
    optional_argumetns = 0
    has_content = True
    final_argument_whitespace = True
    def run(self):
        thenode = tags(text=self.arguments[0])
        return [thenode]

rst.directives.register_directive('tags', Tags)

class abstract(Special, Invisible, FixedTextElement):
    """Directive type declaration for the 'abstract' directive."""
    pass

class Abstract(rst.Directive):
    """
    Defines a 'abstract' docutils node for metadata processing.
    Typically, a brief description of the document in one or two
    complete sentences.  Catches things defined like this:

       .. abstract:: 
          Anerist is a collection of utilities for programatic 
          processing of documentation.


    Content is not rendered.
    """
    required_arguments = 1
    optional_argumetns = 0
    has_content = True
    final_argument_whitespace = True
    def run(self):
        thenode = abstract(text=self.arguments[0])
        return [thenode]

rst.directives.register_directive('abstract', Abstract)

class taxonomy(Special, Invisible, FixedTextElement):
    """Directive type declaration for the 'taxonomy' directive."""
    pass

class Taxonomy(rst.Directive):
    """
    Defines a 'taxonomy' docutils node for metadata processing.
    Possible values should be pre-determined, and separated with
    forward slashes "/".  Used for category assignment, with the
    top of the heirarchy on the left.
    Catches things defined like this:

       .. taxonomy:: Developers/Python/Anerist
    
    Content is not rendered.
    """
    required_arguments = 1
    optional_argumetns = 0
    has_content = True
    final_argument_whitespace = False
    def run(self):
        thenode = taxonomy(text=self.arguments[0])
        return [thenode]

rst.directives.register_directive('taxonomy', Taxonomy)
