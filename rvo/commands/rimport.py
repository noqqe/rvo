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

@click.command('import', short_help="Import documents",
              help="""
              Import documents.
              """)
@click.option('format', '--from', required=False, default="json",
              type=click.Choice(['json', 'markdown', 'mail']),
              help="Specify the format of the input")
@click.option('password', '-p', '--password', required=False, default=False,
              help="Password for encrypted documents")
@click.option('-c', '--category', type=str, multiple=True,
              help='Import to this category')
@click.option('-t', '--tag', type=str, multiple=True,
              help='Import with this tag')
def rimport(format, password, category, tag):
    """ Import to rvo
    :returns: bool
    """

    tags = utils.normalize_element(tag, "tags")
    categories = utils.normalize_element(category, "categories")

    query = {"$and": [ tags, categories ] }

    coll = db.get_document_collection()
    docs = "FOO"

    config = rvo.config.parse_config()

    if format == "json":
        import_json(docs, password)
    if format == "markdown":
        import_markdown(docs, password)
    if format == "mail":
        import_mail(docs, password)

    return True

def import_json(docs, password):
    print("JSON not implemented yet")

def import_markdown(docs, password):
    print("Markdown not implemented yet")

def import_mail(docs, password):
    print("Mail not implemented yet")
