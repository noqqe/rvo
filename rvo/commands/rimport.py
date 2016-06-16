import sys
import click
import email
import quopri
import pprint
import datetime
from bson import ObjectId
from bson.json_util import dumps
import rvo.db as db
import rvo.utils as utils
import rvo.transaction as transaction
from email.header import decode_header
from rvo.crypto import crypto
from rvo.validate import validate
import rvo.config

@click.command('import', short_help="Import documents",
              help="""
              Import documents.
              """)
@click.option('format', '--from', required=False, default="json",
              type=click.Choice(['json', 'mail']),
              help="Specify the format of the input")
@click.option('-c', '--category', type=str, multiple=True,
              help='Import to this category')
@click.option('-t', '--tag', type=str, multiple=True,
              help='Import with this tag')
def rimport(format, category, tag):
    """ Import to rvo
    :returns: bool
    """


    if format == "json":
        import_json()
    if format == "mail":
        import_mail(tag, category)

    return True

def import_json():
    print("JSON not implemented yet")

def import_mail(tag, category):
    content = ""
    for l in click.get_text_stream('stdin'):
        content = content + l
    msg = email.message_from_string(content)

    # title
    subject, encoding = email.header.decode_header(msg['Subject'])[0]
    if encoding is None:
        encoding = "utf-8"

    title = subject.decode(encoding)

    # content
    content = msg.get_payload(decode=False)
    content = quopri.decodestring(content)
    date = datetime.datetime.now()

    coll = db.get_document_collection()
    config = rvo.config.parse_config()

    item = {
        "title": title,
        "content": content,
        "tags": list(tag),
        "categories": list(category),
        "created": date,
        "updated": date,
        "encrypted": False,
    }

    # insert item if its valid
    if validate(item):
        coll = db.get_document_collection()
        docid = coll.insert_one(item).inserted_id

        transaction.log(str(docid), "add", title)
        utils.log_info("Document \"%s\" created." % title)

    else:
        utils.log_error("Validation of the updated object did not succeed")
