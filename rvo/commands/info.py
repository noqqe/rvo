import click
import rvo.db as db
import rvo.transaction as transaction
import rvo.views as views
import rvo.analysis as analysis

@click.command(short_help="Shows metadata of a document",
               help="""
               Shows metadata of a document.

               Metadata matters! NSA kills because of metadata.
               """)
@click.argument('docid')
@click.pass_context
def info(ctx, docid):
    """
    Shows all available meta data belonging to a signel document
    :docid: string (will be converted to bson object)
    :returns: bool
    """
    doc, docid = db.get_document_by_id(ctx, docid)
    transaction.log(ctx, docid, "info", doc["title"])
    views.detail(doc)
    return True
