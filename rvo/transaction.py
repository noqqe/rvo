import datetime
import rvo.db as db

def log(document, type, title):
    """
    Logs any interaction with rvo to the database
    One action generates exactly one entry in the transactions
    collection. The purpose is to be able to track changes
    and see what happens.
    :document: str (objectid)
    :type: str (show, mail, modify, info, add, edit)
    :message:
    :returns: bool
    """
    d = datetime.datetime.now()
    item = {
        "document": document,
        "date": d,
        "type": type,
        "title": title
    }
    db.add_transaction(item)

