import datetime
import click
from bson import ObjectId
import rvo.db as db
import rvo.utils as utils
import rvo.transaction as transaction
from rvo.crypto import crypto
from rvo.cli import validate_date

@click.command(short_help="Modifies a documents metadata",
               help="""
               Modifies a documents meta data.
               See options for what you can modify.

               """)
@click.argument('docid')
@click.option('encrypt', '-e', '--encrypted', default=False, is_flag=True, help='Encrypt this document')
@click.option('tags', '-t', '--tag',
              type=str,
              multiple=True,
              required=False,
              show_default=False,
              help='Set tags for this document')
@click.option('categories', '-c', '--category',
              type=str,
              multiple=True,
              required=False,
              help='Set categories for this document')
@click.option('date', '-d', '--date', default=None,
              help='Set a custom creation date for document', callback=validate_date)
def modify(docid, tags, categories, encrypt, date):
    """
    Modifies a documents meta data
    :docid: str (objectid)
    :tags: list
    :categories: list
    :encrypt: str
    :returns: bool
    """
    coll = db.get_document_collection()
    d = datetime.datetime.now()

    doc, docid = db.get_document_by_id(docid)

    # this is a total crazy hack to get
    # tuple ("a", "b", "c", " ", "d", "e")
    # into
    # list ['abc', 'de']
   # tags = ''.join(list(tags)).split()
    # categories = ''.join(list(categories)).split()
    tags = list(tags)
    categories = list(categories)

    if len(tags) > 0:
        coll.update({"_id": ObjectId(docid)}, {"$set": {"tags": tags, "updated": d}})
        utils.log_info("Updated tags to %s" % ', '.join(tags))
        transaction.log(docid, "tags", doc["title"])

    if len(categories) > 0:
        coll.update({"_id": ObjectId(docid)}, {"$set": {"categories": categories, "updated": d}})
        transaction.log(docid, "category", doc["title"])
        utils.log_info("Updated categories to %s" % ', '.join(categories))

    if encrypt:
        if doc["encrypted"] is False:
            c = crypto()
            content = c.encrypt_content(doc["content"].encode("utf-8"))
            coll.update({"_id": ObjectId(docid)}, {"$set": {"content": content, "encrypted": True}})
            utils.log_info("Document %s is now stored encrypted" % doc["title"])
            transaction.log(docid, "encrypted", doc["title"])
        else:
            utils.log_error("Document %s is already stored encrypted" % doc["title"])

    if not encrypt:
        if doc["encrypted"] is True:
            c = crypto()
            content = c.decrypt_content(doc["content"])
            coll.update({"_id": ObjectId(docid)}, {"$set": {"content": content, "encrypted": False}})
            utils.log_info("Document %s is now stored in plaintext" % doc["title"])
            transaction.log(docid, "decrypted", doc["title"])
        else:
            utils.log_error("Document %s is already stored in plaintext" % doc["title"])

    if date != None:
        coll.update({"_id": ObjectId(docid)}, {"$set": {"created": date, "updated": d}})
        transaction.log(docid, "date", doc["title"])
        utils.log_info("Updated creation date to %s" % date)

    return True
