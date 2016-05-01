import sys
import click
import pprint
from bson import ObjectId
from bson.json_util import dumps
import rvo.db as db
import rvo.utils as utils
import rvo.transaction as transaction
from rvo.crypto import crypto
import rvo.config

@click.command(short_help="Exports all document",
              help="""
              Exports documents.

              In case you want to export some of your documents
              to another piece of code, or build up a website out of
              some of the contents, you can export documents.

              You are free to choose the output format.
              You can also filter on specific documents to export on category
              or on tag.
              """)
@click.option('format', '--to', required=False, default="json",
              type=click.Choice(['json', 'markdown']),
              help="Specify the format of the exported output")
@click.option('password', '-p', '--password', required=False, default=False,
              help="Password for encrypted documents")
@click.option('-c', '--category', type=str, multiple=True,
              help='Exports need to be in this category')
@click.option('-t', '--tag', type=str, multiple=True,
              help='Exports have to contain this tag')
@click.option('objectid', '-i', '--id', type=str, default=False,
              help='Exports document by id')
def export(format, password, category, tag, objectid):
    """
    Shows a single object from database
    and opens its content in a pager
    :docid: string (will be converted to bson object)
    :returns: bool
    """

    if objectid:
        docs = []
        doc, docid = db.get_document_by_id(str(objectid))
        docs.append(doc)
    else:
        if len(category) > 0:
            categories = {"categories": { "$in": category}}
        else:
            categories = {}

        if len(tag) > 0:
            tags = {"tags": { "$in": tag}}
        else:
            tags = {}

        query = {"$and": [ tags, categories ] }

        coll = db.get_document_collection()

        config = rvo.config.parse_config()
        print config

        docs = coll.find(query).sort("updated", -1)

    if format == "json":
        export_json(docs, password)
    if format == "markdown":
        export_markdown(docs, password)

    return True

def export_json(docs, password):
    jsondata = []
    for doc in docs:
        if doc["encrypted"] is True and password is not False:
            c = crypto(password)
            doc["content"] = c.decrypt_content(doc["content"])
        jsondata.append(doc)

    print(dumps(jsondata))

def export_markdown(docs, password):
    for doc in docs:
        if doc["encrypted"] is True and password is not False:
            c = crypto(password)
            doc["content"] = c.decrypt_content(doc["content"])
        else:
            doc["content"] = doc["content"].encode('utf8')

        print doc["content"]
