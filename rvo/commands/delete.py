import click
from bson import ObjectId
import rvo.db as db
import rvo.views as views
import rvo.utils as utils
import rvo.transaction as transaction

@click.command(help="""
               Deletes a document.

               Be careful. Delete means, its gone. Gone gone.
               There is no trashbin whatever. Its like burning a
               piece of paper. Maybe I should configure an alias to 'burn'.
               """)
@click.argument('docid')
@click.option('yes', '-y' ,'--yes', default=False, is_flag=True, help='Dont ask for confirmation')
def delete(docid, yes):
    """
    Deletes a document from the documentstore
    :docid: str (will be converted in bson object)
    :returns: bool
    """
    doc, docid = db.get_document_by_id(docid)
    views.detail(doc)
    coll = db.get_document_collection()

    t = doc["title"]
    if yes:
        coll.remove({"_id": ObjectId(docid)})
        utils.log_info("Removed %s" % t)
    else:
        if click.confirm("%s Are you sure, you want to delete this?" % utils.query_prefix):
            coll.remove({"_id": ObjectId(docid)})
            utils.log_info("Removed %s" % t)
            transaction.log(docid, "delete", t)
            return True

