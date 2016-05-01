import sys
import click
from bson import ObjectId
import rvo.db as db
import rvo.utils as utils
import rvo.transaction as transaction
from rvo.crypto import crypto
from rvo.validate import validate
import rvo.config

@click.command(short_help="Shows a document",
              help="""
              Shows a single document from documentstore
              and opens its content in a pager (or stdout).
              """)
@click.argument('docid')
@click.option('password', '-p', '--password', required=False, default=False,
              help="Password for encrypted documents")
@click.option('stdout', '-s', '--stdout', required=False, default=False, is_flag=True,
              help="Print document to stdout instead of opening pager")
def show(docid, password, stdout):
    """
    Shows a single object from database
    and opens its content in a pager
    :docid: string (will be converted to bson object)
    :returns: bool
    """

    coll = db.get_document_collection()
    doc, docid = db.get_document_by_id(docid)

    config = rvo.config.parse_config()

    if doc["encrypted"] is True:
        c = crypto(password)
        content = c.decrypt_content(doc["content"])
    else:
        content = doc["content"]

    if sys.stdout.isatty() and not stdout:
        utils.view_content_in_pager(config["pager"], template=content)
    else:
        try:
            print(content.encode("utf-8"))
        except UnicodeDecodeError:
            print(content)

    transaction.log(docid, "show", doc["title"])

    # showing the message means decrypting the message
    # in order to do not reuse the nonce from salsa20,
    # we have to reencrypt the content and update the field
    if doc["encrypted"] is True:
        doc["content"] = c.encrypt_content(content)
        if validate(doc):
            coll.save(doc)
        else:
            utils.log_error("Validation of the updated object did not succeed")


    return True

