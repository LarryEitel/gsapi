TODOs
##############

Documents a class, attribute, method, property.

Start on Pseudo code of Dx

Use of GridFS.

Propose mongo indexes and affected fields
    Place a # index above field

Post Save of Document
Post Index of Document
    Using a external class to handle base indexing with ability to override on extended model classes.

QUESTION: Suggestions Comments regarding logging events and additionally enabling undo/rollback of changes?

Must read and note relavent points:
    http://api.mongodb.org/python/current/faq.html
    http://docs.mongodb.org/manual/use-cases/hierarchical-aggregation/
    

How to autodocument a python module using Sphinx?

Create a sphinx project.
Create a sample python file. For example,

class Test():
  '''Hi This is a sample class'''

  var = 7
  '''An integer variable'''

  def __init__(self):
    '''**Constructor**'''
    print "test"

  @property
  def xyz(self):
    '''A sample property :math:`e^{i\pi}+1=0`'''
    pass

In the docstrings you can write all valid reStructuredText elements.

Now craete a rst file. For example,

test
****
.. automodule:: test
.. autoclass:: Test
  :members:
  :undoc-members:
  :private-members:
  :special-members:
.. autofunction:: __init__


Run make and voila! You code is documemented.

To learn about all possible autodoc functionality please visit http://sphinx-doc.org/ext/autodoc.html
