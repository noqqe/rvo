import click
import rvo.db as db
import rvo.utils as utils
import rvo.transaction as transaction
import rvo.config
import simplemail


@click.command(short_help="Mails a document to a recipient for your choice",
               help="""
    Mails a document to a recipient for your choice.
    Its required to have a local unauthenticated smtpd running
    otherwise sending mails will fail.

    Im so s0rr3y.
    """)
@click.option('to', '-t', '--to', type=str, prompt="%s To" % utils.query_prefix,
              help='Recipient of the mail')
@click.argument('docid')
def mail(docid, to):
    """
    Mails a document to a recipient for your choice
    Its required to have a local unauthenticated smtpd running
    otherwise sending mails will fail
    :docid: str (Bson Object)
    :returns: bool
    """

    coll = db.get_document_collection()
    config = rvo.config.parse_config()
    doc, docid = db.get_document_by_id(docid)

    try:
        simplemail.Email(
            smtp_server = "localhost",
            from_address = config["mailfrom"],
            to_address = to,
            subject = unicode(doc["title"]),
            message = doc["content"].encode("utf-8")
        ).send()
    except:
        utils.log_error("Error trying to send mail. May check your configuration.")
