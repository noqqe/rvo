import re
import click
import datetime
from dateutil.relativedelta import relativedelta
import rvo.db as db
import rvo.utils as utils
import rvo.views as views
from rvo.cli import validate_date

@click.command(short_help="Some nostalgia by showing documents some years ago",
               help="""
               The memories command shows documents that were
               created exactly one (or more..) years ago today.

               \b
               Hint: This can be used to send an email to you for
               some entertainment.

               """)
@click.option('format', '--format', '-f',
              type=click.Choice(['table', 'detail']), default='table',
              help='Results by date ending at date')
def memories(format):
    """
    :format: str
    :returns: bool
    """
    coll = db.get_document_collection()

    documents = {}

    for year in reversed(range(1,40)):
        start = datetime.datetime.now() - relativedelta(years=year)
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = datetime.datetime.now() - relativedelta(years=year,days=-1)
        end = end.replace(hour=0, minute=0, second=0, microsecond=0)

        query = {"$and": [ {"created": {'$gte': start, '$lt': end}} ]}

        if coll.find(query).count():
            utils.log_info("%s year(s) ago today:\n" % year)
        else:
            continue

        if format == "table":
            limit = 0
            docs = coll.find(query)

            for doc in docs:
                limit += 1
                documents[limit] = doc

            db.clean_shortids()

            for x in reversed(range(1, limit+1)):
                db.map_shortid(sid=x, oid=documents[x]["_id"])
                documents[x]["sid"] = x

            views.table(documents, limit+1)

            limit = 0

        if format == "detail":
            docs = coll.find(query)
            for doc in docs:
                views.detail(doc)


    return True
