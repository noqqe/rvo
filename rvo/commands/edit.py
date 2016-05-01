import click
import datetime
from bson import ObjectId
import rvo.db as db
import rvo.utils as utils
import rvo.transaction as transaction
from rvo.crypto import crypto
from rvo.validate import validate
import rvo.config

@click.command(help="""
               Edit the content of an document.

               Your configured editor will be opened and you
               are free to type any content you like.
               Once you save and close the editor, content will be
               read and added to the store.

               If the content does not get changed, rvo detects
               there was no change and does not update.
               """)
@click.argument('docid')
@click.option('password', '-p', '--password', required=False, default=False,
              help="Password for encrypted documents")
def edit(docid, password):
    """
    Edit the content of an document.
    Trys to find the object, (decrypt,) read from editor,
    encrypt, update date fields and regenerates the title.
    :docid: str (bson object)
    :returns: bool
    """
    coll = db.get_document_collection()
    config = rvo.config.parse_config()

    doc, docid = db.get_document_by_id(docid)
    title = doc["title"]

    if doc["encrypted"] is True:
        c = crypto(password)
        template = c.decrypt_content(doc["content"])
        if template is False:
            return False
    else:
        template = doc["content"]

    content, tmpfile = utils.get_content_from_editor(config["editor"], template=template)
    d = datetime.datetime.now()

    if doc["encrypted"] is True:
        title = utils.get_title_from_content(content)
        content = c.encrypt_content(content)
    else:
        if not "links" in doc["categories"]:
            title = utils.get_title_from_content(content)

    if isinstance(template, unicode):
        content = content.decode("utf-8")

    if content != template:

        doc["content"] = content
        doc["title"] = title
        doc["updated"] = d
        if validate(doc):
            coll.save(doc)
        else:
            utils.log_error("Validation of the updated object did not succeed")

        transaction.log(docid, "edit", title)
        utils.log_info("Document \"%s\" updated." % title)
    else:
        utils.log_info("No changes detected for \"%s\"" % title)

    utils.clean_tmpfile(tmpfile)

    return True
