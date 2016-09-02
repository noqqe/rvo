import sys
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
import rvo.config

@click.command(short_help="Text analysis on a document",
               help="""
               To be honest, I just wanted to play with nltk.
               Also i like statistics and this kind of stuff.

               So this will print out some natrual language facts about
               the document given.
               """)
@click.option('password', '-p', '--password', required=False, default=False,
              help="Password for encrypted documents")
@click.option('-c', '--category', type=str, multiple=True,
              help='filter for category')
@click.option('-t', '--tag', type=str, multiple=True,
              help='filter for tags')
@click.option('objectid', '-i', '--id', type=str, default=False,
              help='only on a single document by id')
@click.pass_context
def stats(ctx, objectid, category, tag, password):
    """
    :docid: str
    :returns: bool
    """

    coll = db.get_document_collection(ctx)

    if objectid:
        docs = []
        doc, docid = db.get_document_by_id(ctx, str(objectid))
        docs.append(doc)
    else:
        tags = utils.normalize_element(tag, "tags")
        categories = utils.normalize_element(category, "categories")
        query = {"$and": [ tags, categories ] }
        coll = db.get_document_collection(ctx)

        config = ctx.obj["config"]

        docs = coll.find(query).sort("updated", -1)

    content = ""
    tags = []
    categories = []
    c = False
    for doc in docs:
        if c is False:
            doc["content"],c = db.get_content(ctx, doc, crypto_object=c, password=password)

        content += doc["content"]
        tags.extend(doc["tags"])
        categories.extend(doc["categories"])

    if len(content) == 0:
        utils.log_error("No documents found with this query")
        return False


    utils.log_info("Text analysis\n")
    table = []
    headers = ["Analysis", "Result"]

    try:
        analysis.get_sentences("this is a test")
    except LookupError:
        utils.log_error("NLTK is needed to do text analysis on your document")
        utils.log_error("In order to do this, execute:")
        utils.log_error(' python -c \'import nltk; nltk.download("book")\'')
        sys.exit(1)

    table.append(["Sentences" , analysis.get_sentences(content)])
    table.append(["Words", analysis.get_words(content)])
    table.append(["Characters", analysis.get_characters(content)])
    table.append(["Tags", len(tags)])
    table.append(["Categories", len(categories)])
    table.append(["Size of documents", analysis.get_size_of_document(content)])
    if objectid:
        table.append(["Age of document", analysis.get_age_of_document(doc["created"])])

    cwords = ""
    fdist = analysis.get_word_distribution(content)

    for w, f in analysis.get_most_common_words(fdist, 5):
        cwords = cwords + w + "(" + str(f) + ") "
    table.append(["Most common words", cwords])

    lwords = ""
    for f in analysis.get_least_common_words(fdist, 5):
       lwords = lwords + " " + f
    table.append(["Least common words", lwords])
    table.append(["Words per sentence", analysis.get_words_per_sentence(content)])

    longwords = ""
    for f in analysis.get_long_words(fdist, 5):
       longwords = longwords + " " + f
    table.append(["Long words", longwords])

    print tabulate(table, headers=headers)
    print("")

    return True
