import click
import datetime
import rvo.db as db
import rvo.utils as utils

@click.command(short_help="Show statistics about categories and tags",
               help="""
                Show statistics about categories and tags
                of your documents.

                So number of tags, categories, posts per year
                and other insignificant data will be shown.
               """)
def stats():
    """
    Show statistics about categories and tags
    of your documents.
    :returns: True
    """
    coll = db.get_document_collection()

    for cat in coll.distinct("categories"):
        utils.log_info(cat)
        num = coll.find({"categories": cat}).count()
        print("total: %s" % (num))
        w = 0
        z = 0

        for doc in coll.find({"categories": cat}):
            w += len(''.join(c if c.isalnum() else ' ' for c in doc["content"]).split())
            z += len(doc["content"])

        print("words: %s" % w)
        print("chars: %s" % z)

        tags = coll.find({"categories": cat},{"tags": 1})
        mlist = []
        tagcount = 0
        for t in tags:
            mlist = list(set(mlist + t["tags"]))
            tagcount += len(t["tags"])

        print("tags: %s" % tagcount)
        print("unique tags: %s" % len(mlist))

        for x in range(1970, 2018):
            start = datetime.datetime(x, 1, 1, 0, 0, 0, 557000)
            end = datetime.datetime(x + 1, 1, 1, 0, 0, 0, 557000)
            y = coll.find({"$and":
                            [ {"created": {'$gt': start, '$lt': end}},
                              {"categories": cat}
                            ]
                        }).count()
            if y > 0:
                print(" %s: %s" % (x,y))
        print("")

    utils.log_info("total")
    num = coll.find({}).count()
    print("documents: %s" % (num))

    for doc in coll.find({}):
        w += len(''.join(c if c.isalnum() else ' ' for c in doc["content"]).split())
        z += len(doc["content"])

    print("words: %s" % w)
    print("chars: %s" % z)

    return True
