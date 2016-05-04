.. image:: https://travis-ci.org/noqqe/rvo.svg?branch=master
    :target: https://travis-ci.org/noqqe/rvo

.. image:: https://codecov.io/gh/noqqe/rvo/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/noqqe/rvo

.. image:: https://codeclimate.com/github/noqqe/rvo/badges/gpa.svg
   :target: https://codeclimate.com/github/noqqe/rvo
   :alt: Code Climate

rvo
===

I use ``rvo`` for managing my text data.

-  Notes
-  Docs (personal wiki)
-  Bookmarks
-  Journal
-  Quotes

and the like.

Motivations
~~~~~~~~~~~

When I started writing rvo, my goal was designing an utility that feels
a little like markdown. It should be usable very easily. A handy program
the user likes to use. At the same time it should be easy to
integrate with other tools. Taking the typical unix approach. Make it
read and write to stdin/out. Have it fully configurable with commandline
parameters.

It basically should not matter if a human or a machine is interacting
with ``rvo``.

Features
~~~~~~~~

-  Rich search capabilities
-  Statistics about the documents
-  Encryption of single documents using Salsa20 and Blake2b
-  Interacts with ``vim``
-  Fetching the title of a link to be the title of your document
-  Mail an article to a friend of yours.
-  Easily interact with other programs using stdin / stdout

Installation
~~~~~~~~~~~~

::

    pip install rvo

After that, setup a mongodb. You may use your favorite packagemanager.
For me it's OpenBSDs "pkg_add".

::

		/etc/init.d/mongod start

Configuration
~~~~~~~~~~~~~

::

    [General]
    MongoDB = mongodb://localhost/
    DB = rvo
    Editor = vim
    Pager = vim -R
    MailFrom = user@example.net

After it was successfully configured, run ping to verfiy
the connection to mongodb works.

::

		$ rvo ping
		>>> Trying to connect to database...
		>>> Connection SUCCESSFUL
		>>> Trying to write, read, delete to test_collection...
		>>> Interactions were SUCCESSFUL

Quickstart
~~~~~~~~~~

`rvo` is a really friendly piece of software. It helps you whereever it needs to.
You may start with a simple

::

		$ rvo --help

To add a document, just

::

		$ rvo add

and tada, your very first document is created. Add content from whatever you like. As said before,
you can store notes, write diary. After that, check out your documents.

::

    $ rvo list


Thats all. Just kidding. Have a look into all the the other commands!

::

 		add       Add a document.
 		analyze   Text analysis on a document
 		append    Append content to a document.
 		delete    Deletes a document.
 		edit      Edit the content of an document.
 		export    Exports all document
 		info      Shows metadata of a document
 		list      List documents from store
 		log       Show transactions
 		mail      Mails a document to a recipient for your choice
 		memories  Some nostalgia by showing documents some years ago
 		modify    Modifies a documents metadata
 		ping      Verifys the connection to the database
 		show      Shows a document
 		stats     Show statistics about categories and tags

Document titles
~~~~~~~~~~~~~~~

The title from a normal document is generated from the first line of the
content. Leading whitespace and ``#`` will be stripped away.

::

    $ rvo add -t javascript -c notes
    # Meeting Notes

    * We should probably throw away our .js applications
    * ...

So "Meeting Notes" will be the document title. This also happens when you edit
a document. So if you want to change the title, edit the content and after
saving the title gets updated.

Stdout
~~~~~~

Normally, ``rvo`` opens your favorite ``PAGER``. If output redirection
is detected it just outputs plain content to whatever file you like.

::

    $ rvo list -c meeting
    $ rvo show 1 > /tmp/meeting.md

Also without redirection the content is being ``cat`` ed by using the ``-s`` flag

::

    $ rvo show -s 2

Stdin
~~~~~

Read content from stdin

::

    $ echo foo | rvo add -t test -c notes

Export
~~~~~~

You can easily export all what you've inserted.

::

    rvo export -c twitter --to json | python -m json.tool
    rvo export -t work --to markdown

Or just loop over the output

::

    rvo list -l 5000
    for x in {1..5000} ; do rvo show --stdout $x ; done

Document identification
~~~~~~~~~~~~~~~~~~~~~~~

As a typical workflow, you do a list query and You can either use the
full mongodb objectid or a shortid.

Everytime you do a list query, a resultset will be built. Every result
gets a shortid assigned to it and this mapping is being saved in
mongodb.

I've implemented shortids because they are easier to use. You dont have
to copy the full objectid using copy with mouse. ``shortids`` are easier
to use!

Crypto
~~~~~~

The crypto used is written with `Salsa20` and `blake2b`. When the first
document is created and being encrypted, rvo prompts for the initial password.
Keep this password save. You will need it more often.

The password you set is used to encrypt a randomly generated character long
password. Its stored within the database. Most important. The generated password
is used to encrypt and decrypt every document (when encryption is set).

Basically that means: there is one password (chosen by you) that unlocks
another generated password, that encrypts your document.

This ensures a lot of stuff. For example easy password changes for the user.
Or setting a slightly different password accidentially for one document.


Links
~~~~~

Links: If the content is just an url, it gets automatically the category
``links`` and its html title will be fetched to be used as ``title``
within the document.

Development
-----------

Wording.

-  docid is what is being used to identify a document. It can be both, a
   shortid or a ObjectId (MongoDB)

-  Documentstore basically means mongodb at the moment

-  All commands have to be stored in submodule commands and can contain
   only 1 command that has to be named exactly as the filename is. This
   is required for click to parse all commands.

Data Structure
~~~~~~~~~~~~~~

The native json document that goes into MongoDB looks like this

::

    {
      "_id" : ObjectId("568d344c6815b45596d1c7ad"),
      "title": "My very first entry"
      "content" : "<Markdown Content goes here>",
      "created": ISODate("2014-09-03T07:37:52Z"),
      "updated": ISODate("2015-09-03T07:37:52Z"),
      "tags": [ "mongodb", "markdown" ],
      "category": ["notes"],
      "encrypted": false,
    }

Since rvo uses ``pymongo``, its way easier dealing with documents.
Python native types are automatically converted to the corresponding
types in json/mongodb. The following is a native python dictionary.

::

    {
      'title': '2-Factor-Auth',
      'content': '<Markdown Content goes here>',
      'created': datetime.datetime(),
      'updated': datetime.datetime(),
      'tags': ['markdown, 'mongodb'],
      'encrypted': False,
      'categories': ['notes'],
    }

Missing
~~~~~~~

There are also features, that rvo does not have and probably never gets.

-  Version control for your documents
-  Multiple users or an "author" field.

Last but not least
~~~~~~~~~~~~~~~~~~

Do not confuse `rvo` with http://www.rvo.nl. Rijksdienst voor Ondernemend Nederland.
It has nothing to do with it. Still, I really like their logo.
