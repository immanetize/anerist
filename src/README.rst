=============
 the Anerist
=============
---------------------------------------
 the documentation indifference engine
---------------------------------------
This "ansible" branch contains a somewhat reusable ansible configuration for testing.  A distributable rendition of anerist's python modules is maintained in the master branch.  

The master branch is mostly maintained via `ghp-import -b master files/anerist` and so the anerist branch will have the most informative changelog.  Please send your patches against this branch for now.

    The Aneristic Principle is that of APPARENT ORDER; the Eristic
    Principle is that of APPARENT DISORDER. Both order and disorder are man made
    concepts and are artificial divisions of PURE CHAOS, which is a level deeper
    that is the level of distinction making.

    -- A monkey

Anerist is a collection of Python scripts for buildbot.  It processes documentation of a variety of formats and generates a website frontend for browsing all processed docs.

Command line utility
======================
The `/usr/bin/anerist` utility has some functions for processing documents.  Buildbot likes buildsteps to be executable commands, not raw python code.


Builder roles
================

For each known markup format, Anerist provides four types of BuildSteps for processing

Validation
------------
A validation factory ingests changes from VCS and builds the document to test them.  It may integrate unit tests such as those offered by `emender <https://github.com/emender/emender>`_.

If a build is successfully validated, new strings are generated for translation and pushed to a translation platform, currently Zanata.

Integration
-------------
An integration factory pulls translations from a centralized translation platform like Zanata and tests them.  If the translated document is built successfully, the translations are committed to version control.

Identification
----------------
Metadata that describes the work is extracted from the content.  This information is used during the Assembly process to determine site structure present the document.

Production
------------
A production factory builds the content in a format designed for web viewing and pushes it to a central location for later processing by the Assembler.



The Assembler
===============
The Assembler processes a directory containing all production builds of all known documentation.  It does not yet exist.

