import re
import click
import datetime
from dateutil.relativedelta import relativedelta
import rvo.db as db
import rvo.utils as utils
import rvo.views as views
from rvo.cli import validate_date
import rvo.analysis as analysis
from rvo.crypto import crypto
from rvo.validate import validate
from tabulate import tabulate

@click.command(short_help="Text analysis on a document",
               help="""
               To be honest, I just wanted to play with nltk.
               Also i like statistics and this kind of stuff.

               So this will print out some natrual language facts about
               the document given.
               """)
@click.option('password', '-p', '--password', required=False, default=False,
              help="Password for encrypted documents")
@click.argument('docid')
def analyze(docid, password):
    """
    :docid: str
    :returns: bool
    """

    doc, docid = db.get_document_by_id(docid)
    coll = db.get_document_collection()

    if doc["encrypted"] is True:
        c = crypto(password)
        content = c.decrypt_content(doc["content"])
        content = content.decode("utf-8")
    else:
        content = doc["content"]

    print("")
    print(doc["title"] + "\n")

    table = []
    headers = ["Analysis", "Result"]

    table.append(["Sentences" , analysis.get_sentences(content)])
    table.append(["Words", analysis.get_words(content)])
    table.append(["Characters", analysis.get_characters(content)])
    table.append(["Tags", len(doc["tags"])])
    table.append(["Categories", len(doc["categories"])])
    table.append(["Age of document", analysis.get_age_of_document(doc["created"])])
    table.append(["Size of document", analysis.get_size_of_document(doc["content"])])

    cwords = ""
    for w, f in analysis.get_most_common_words(content, 5):
        cwords = cwords + w + "(" + str(f) + ") "
    table.append(["Most common words", cwords])

    lwords = ""
    for f in analysis.get_least_common_words(content, 5):
       lwords = lwords + " " + f
    table.append(["Least common words", lwords])
    table.append(["Words per sentence", analysis.get_words_per_sentence(content)])

    longwords = ""
    for f in analysis.get_long_words(content, 5):
       longwords = longwords + " " + f
    table.append(["Long words", longwords])

    print tabulate(table, headers=headers)
    print("")

    if doc["encrypted"] is True:
        content = content.encode("utf-8")
        doc["content"] = c.encrypt_content(content)
        if validate(doc):
            coll.save(doc)
        else:
            utils.log_error("Validation of the updated object did not succeed")

    return True
