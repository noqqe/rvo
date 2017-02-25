import re
import click
import datetime
from dateutil.relativedelta import relativedelta
import rvo.db as db
import rvo.utils as utils
import rvo.views as views
from rvo.validate import validate_date

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
@click.option('date', '-d', '--date', default=datetime.datetime.now(),
              help='Set a custom creation date for document', callback=validate_date)
@click.pass_context
def memories(ctx, format, date):
    """
    :format: str
    :returns: bool
    """
    coll = db.get_document_collection(ctx)

    documents = {}

    limit = 0
    utils.log_info("Documents having birthday today.\n")
    for year in range(1,40):
        start = date - relativedelta(years=year)
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = date - relativedelta(years=year,days=-1)
        end = end.replace(hour=0, minute=0, second=0, microsecond=0)

        query = {"$and": [ {"created": {'$gte': start, '$lt': end}} ]}

        if format == "table":
            docs = coll.find(query)

            for doc in docs:
                limit += 1
                documents[limit] = doc


        if format == "detail":
            docs = coll.find(query)
            for doc in docs:
                views.detail(doc)

    # If not detail view - print all memories in one table
    if format == "table":
        db.clean_shortids(ctx)
        for x in reversed(range(1, limit+1)):
            db.map_shortid(ctx, sid=x, oid=documents[x]["_id"])
            documents[x]["sid"] = x

        views.table(documents, limit+1)


    return True
