import re
import click
import datetime
import rvo.db as db
import rvo.utils as utils
import rvo.views as views
from rvo.cli import validate_date

@click.command(short_help="List documents from store",
               help="""
               Lists documents from the documentstore

               By default, the 10 latest documents will be shown.
               As documents grow, it gets difficult to find those.

               Filters can be applied on list command.
               See options below on how to filter the output.

               """)
@click.option('-t', '--tag', type=str, multiple=True,
              help='Results have to contain this tag')
@click.option('-c', '--category', type=str, multiple=True,
              help='Results need to be in this category')
@click.option('-s', '--title', type=str, multiple=True,
              help='Results need to contain this string in title')
@click.option('-x', '--content', type=str, multiple=True,
              help='Results need to contain this string in content')
@click.option('-l', '--limit', type=int, default=10,
              help='Limit the number of results')
@click.option('datefrom', '-f', '--from', default=datetime.datetime.utcfromtimestamp(0),
              callback=validate_date,
              help='Results by date starting from')
@click.option('dateto', '-d', '--to', default=datetime.datetime.now(),
              callback=validate_date,
              help='Results by date ending at date')
def list(tag, category, title, content, limit, dateto, datefrom):
    """
    Lists documents from database based on the filters
    given. First stage is triggering the filter parser,
    building the query and finally printing results by
    calling the view.
    :filters: string (formatted as l:foo or x:bar)
    :returns: bool
    """
    coll = db.get_document_collection()

    if len(tag) > 0:
        tags = {"tags": { "$in": tag}}
    else:
        tags = {}

    if len(category) > 0:
        categories = {"categories": { "$in": category}}
    else:
        categories = {}

    if len(title) > 0:
        titles = []
        for t in title:
            titles.append(re.compile(t, re.IGNORECASE))
        titles = {"title": { "$in": titles}}
    else:
        titles = {}

    if len(content) > 0:
        contents = []
        for c in content:
            contents.append(re.compile(c, re.IGNORECASE))
        contents = {"content": { "$in": contents}}
    else:
        contents = {}

    df = { "updated": { "$gte": datefrom }}
    de = { "updated": { "$lte": dateto }}

    query = {"$and": [ tags, categories, contents, titles, de, df ] }

    print("")
    documents = {}
    c = 0

    # Fetch results from collection and feed it into a numbered
    # dictonary
    for doc in coll.find(query).sort("updated", -1).limit(limit):
        c += 1
        documents[c] = doc

    # If there are less entries in collection
    # then the limit is, overwrite limit with c
    if c < limit:
        limit = c

    db.clean_shortids()
    # reverse the order using the numbered keys
    # and display the object
    for x in reversed(range(1, limit+1)):
        db.map_shortid(sid=x, oid=documents[x]["_id"])
        documents[x]["sid"] = x

    views.table(documents, limit+1)

    # print summary of results
    results = coll.find(query).sort("created", -1).count()
    utils.log_info("%s out of %s result(s)." % (len(documents), results))

    return True
