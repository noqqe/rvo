#!/usr/bin/env python2.7
"""
Views are the rendering part. A dict object (most likly from mongodb)
will be displayed in a human readable, colorized way
"""
from tabulate import tabulate

def colorize(ty, msg):
    """
    Will colorize a given message using
    a color scheme (prompt) of a given type.
    :ty: str (type of colorizations)
    :msg: str (content to colorize)
    :returns: str (full colorized)
    """

    reset = '\033[0m'
    if ty == "title":
       pre = '\033[38;5;118m'
    if ty == 'tags':
       pre = '\033[38;5;97m'
    if ty == 'cats':
       pre = '\033[38;5;121m'
    if ty == 'header':
       pre = '\033[38;5;15m'

    return pre + msg + reset

def display_tags(tags):
    """
    Display tags if they are available
    :tags: list
    :returns: bool
    """
    print("tags:"),
    for e in tags:
        print(colorize(msg=e,ty="tags")),
    return True

def display_categories(cat):
    """
    Display categories if they are available
    :cat: list
    :returns: bool
    """
    print(" cats:"),
    for e in cat:
        print(colorize(msg=e,ty="cats")),
    return True

def table(documents, size):
    # print documents
    table = []
    headers = [
        colorize(msg="ID", ty="header"),
        colorize(msg="Title", ty="header"),
        colorize(msg="Cats", ty="header"),
        colorize(msg="Tags", ty="header"),
        colorize(msg="Date", ty="header")
    ]

    for x in reversed(range(1,size)):

        y = [
            documents[x]["sid"],
            colorize(msg=documents[x]["title"][0:60], ty="title"),
            colorize(msg=' '.join(documents[x]["categories"]), ty="cats"),
            colorize(msg=' '.join(documents[x]["tags"]),ty="tags"),
            documents[x]["created"].strftime("%Y-%m-%d")
        ]
        table.append(y)

    print tabulate(table, headers=headers)
    print ""

def detail(doc):
    """
    Display a single object using eventually meta
    wrappers from above with all meta data that exist.
    :r: dict (document from database)
    :returns: bool
    """

    # ID
    print("")
    print("   id: " + str(doc["_id"]))

    # Title
    print("title:"),
    print(colorize(msg=doc["title"],ty="title"))
    print(""),

    # Tags
    try:
        display_tags(doc["tags"])
    except KeyError:
        pass
    print("")

    # Categories
    try:
        display_categories(doc["categories"])
    except KeyError:
        pass
    print("")

    # Date
    print(" date: " + doc["created"].strftime('%Y-%m-%d %H:%M'))
    print("  mod: " + doc["updated"].strftime('%Y-%m-%d %H:%M'))
    print("  enc: " + str(doc["encrypted"]))

    # URL
    if any("links" in s for s in doc["categories"]):
        print("  url: " + doc["content"])

    print("")

    return True

def transactions(documents, size):
    """
    Display a single object using eventually meta
    wrappers from above
    :r: dict (document from database)
    :returns: bool
    """

    # print documents
    table = []
    headers = [
        colorize(msg="Date", ty="header"),
        colorize(msg="Type", ty="header"),
        colorize(msg="Title", ty="header"),
        colorize(msg="ObjectId", ty="header"),
    ]

    for x in reversed(range(1,size)):

        y = [
            documents[x]["date"].strftime("%Y-%m-%d %H:%M"),
            colorize(msg=documents[x]["type"], ty="cats"),
            colorize(msg=documents[x]["title"], ty="title"),
            str(documents[x]["_id"]),
        ]
        table.append(y)

    print tabulate(table, headers=headers)
    print ""

    return True
