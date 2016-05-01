import click
import datetime
from bson import ObjectId
import rvo.db as db
import rvo.utils as utils
import rvo.transaction as transaction
from rvo.crypto import crypto
from rvo.validate import validate

@click.command(help="""
               Append content to a document.
               This is useful for programmatically adding content.
               """)
@click.option('password', '-p', '--password', required=False, default=False,
              help="Password for encrypted documents")
@click.option('content', '-x', '--content', required=False, default=False,
              help="Content to be appended to the document")
@click.argument('docid')
def append(docid, password, content):
    """
    Append string to a document

    Trys to find the object, (decrypt,) adds content to the bottom,
    (encrypt,) update date fields and regenerates the title.

    :docid: str (bson object)
    :returns: bool
    """

    coll = db.get_document_collection()

    doc, docid = db.get_document_by_id(docid)

    if doc["encrypted"] is True:
        c = crypto(password)
        template = c.decrypt_content(doc["content"])
        template = template.decode("utf-8")
    else:
        template = doc["content"]

    d = datetime.datetime.now()

    if not content:
        content = ""
        for l in click.get_text_stream('stdin'):
                content = content + l

    content = template + content

    if isinstance(content, unicode):
        content = content.encode("utf-8")

    if doc["encrypted"] is True:
        title = utils.get_title_from_content(content)
        content = c.encrypt_content(content)
    else:
        if not "links" in doc["categories"]:
            title = utils.get_title_from_content(content)


    if content != template:
        doc["content"] = content
        doc["title"] = title
        doc["updated"] = d
        if validate(doc):
            coll.save(doc)
            transaction.log(docid, "append", title)
            utils.log_info("Content appended to \"%s\"." % title)
        else:
            utils.log_error("Validation of the updated object did not succeed")
    else:
        utils.log_info("No changes detected for \"%s\"" % title)

    return True
