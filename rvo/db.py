import sys
import pymongo
import bson
from bson.objectid import ObjectId
import rvo.utils as utils
import rvo.config

def db_ping(ctx):
    """ Ping the connection to mongodb database
    :returns: bool
    """
    try:
        config = ctx.obj["config"]
        c = ctx.obj["db"]
        c.server_info()
        return True
    except:
        return False

def db_verify(ctx):
    """ Does a test write, read and remove
    :returns: bool
    """
    try:
        # Define name
        testcoll = "test_collection"

        # Fetch config and get db object
        config = ctx.obj["config"]
        c = ctx.obj["db"]
        db = c[config["db"]]

        # Get collection object
        coll = get_collection(ctx, testcoll)

        # Do write test
        coll.insert({"a": 1})

        # Do read test
        resp = coll.find_one({})
        if resp == {"a": 1}:
            pass

        # Do removal test
        coll.remove({})

        # Drop test_collection
        db.drop_collection(testcoll)

        return True
    except:
        return False

def get_collection(ctx, coll):
    """ Initialize MongoDB Connection
    :returns: collection object
    """
    config = ctx.obj["config"]
    c = ctx.obj["db"]
    db = c[config["db"]]
    collection = db[coll]
    return collection

def get_document_collection(ctx):
    """
    Get document collection handle
    from config.
    :returns: collection object
    """
    config = ctx.obj["config"]
    collection = get_collection(ctx, config["collection"])
    return collection

def get_transactions_collection(ctx):
    """
    Get document collection handle
    from config.
    :returns: collection object
    """
    config = ctx.obj["config"]
    collection = get_collection(ctx, config["transactions"])
    return collection

def get_config_collection(ctx):
    """
    Get document collection handle
    from config.
    :returns: collection object
    """
    config = ctx.obj["config"]
    collection = get_collection(ctx, config["config"])
    return collection

def get_shortids_collection(ctx):
    """
    Get document collection handle
    from config.
    :returns: collection object
    """
    config = ctx.obj["config"]
    collection = get_collection(ctx, config["shortids"])
    return collection

def check_for_duplicate(ctx, field, content):
    """ Check if url already exists in db
    :returns: bool
    """
    config = ctx.obj["config"]
    coll = get_collection(ctx, config["collection"])

    if coll.find({field: content}).count() > 0:
        return True
    else:
        return False

def get_document_by_id(ctx, id):
    """
    Gets a document by its id, exits if false
    :coll: pymongo collection object
    :id: str
    :returns: dict, docid
    """
    coll = get_document_collection(ctx)
    shortids = get_shortids_collection(ctx)

    try:
        doc = shortids.find_one({"sid": int(id)})
        id = str(doc["oid"])
    except (IndexError, ValueError, TypeError) as e:
        pass

    try:
        doc = coll.find_one({"_id": ObjectId(id)})
        if doc is None:
            utils.log_info("No Results for %s" % id)
            sys.exit(1)
        return doc, id
    except bson.errors.InvalidId:
        utils.log_error("Error: %s is not a valid ID or ObjectId." % id)
        sys.exit(1)

def map_shortid(ctx, sid, oid):
    """
    Maps oid to a short id for better usage
    in commandline. At the end you have to type
    "edit 2" and not "edit 56823D28ds23821"
    Mapping will be stored in a separate collection
    and should be resettet with each view.
    :coll: pymongo collection object
    :sid: str (bson object id)
    :oid: str (bson object id)
    :returns: dict
    """
    shortids = get_shortids_collection(ctx)
    shortids.insert({"sid": sid, "oid": oid})
    return True

def clean_shortids(ctx):
    """
    Cleans all shortids from cache collection.
    Necessary to get fresh results for every search
    :coll: pymongo collection object
    :returns: bool
    """
    shortids = get_shortids_collection(ctx)
    shortids.remove({"$and": [{"sid": {"$exists": True}}, {"oid": {"$exists": True}}]})
    return True

def add_transaction(ctx, item):
    transactions = get_transactions_collection(ctx)
    transactions.insert(item)
    return True

def get_content(ctx, doc, crypto_object=False, password=False):
    """
    Get content of a document.
    For later use, it also returns the initialized crypto object
    :doc: document object
    :crypto_object: instance of class rvo.crypto.crypto
    returns: str, crypto_object
    """
    from rvo.crypto import crypto
    c = crypto_object
    if doc["encrypted"] is True:
        if c is False:
            c = crypto(ctx=ctx, password=password)
        content = c.decrypt_content(doc["content"])
        content = content.decode("utf8")
    else:
        content = doc["content"]

    return content, c
