import click
import rvo.db as db
import rvo.views as views

@click.command(short_help="Show transactions",
               help="""
               Transactions are logged informations
               about changes and access to the documents.

               `log' is used to get those transactions listed.

               Having a hard time remembering what you did?
               """)
@click.option('entries', '-e', '--entries', default=15, type=int,
              help='Number of entries being shown')
def log(entries):
    """
    Shows n latest transactions
    :n: int
    :returns: bool
    """
    coll = db.get_transactions_collection()

    SUM = {}
    c = 0
    print("")
    for doc in coll.find({}).sort("date", -1).limit(entries):
        c += 1
        SUM[c] = doc

    views.transactions(SUM, c+1)

    return True

