
import re
import sys
import pytest
from click.testing import CliRunner
from rvo import cli
import rvo.commands.add
import rvo.commands.list
import datetime
import rvo.config
import mongomock
from bson import ObjectId
from dateutil import parser

def mock_documents_collection():

    docs = []

    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce7bdb583"),
        "updated" : parser.parse("2015-02-01"),
        "encrypted" : False,
        "created" : parser.parse("2015-02-01"),
        "content" : "# Nutella, Coffee, ninja\n\nNutrlla, Horst, hadoop\n",
        "title" : "Nutella, Coffee, ninja",
        "categories" : [ "notes" ],
        "tags" : [ "list", "todo" ] })
    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce7bdb584"),
        "updated" : parser.parse("2016-03-05"),
        "encrypted" : False,
        "created" : parser.parse("2016-03-01"),
        "content" : "just broke my leg\n",
        "title" : "Whoop Whoop",
        "categories" : [ "jrnl" ],
        "tags" : [ "holiday", "vacation" ] })
    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce7bdb585"),
        "updated" : parser.parse("2004-04-04"),
        "encrypted" : False,
        "created" : parser.parse("2004-04-01"),
        "content" : "just broke my leg again\n",
        "title" : "Whoop Whoop Reloaded",
        "categories" : [ "jrnl" ],
        "tags" : [ "holiday", "vacation" ] })
    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce7bdb586"),
        "updated" : parser.parse("1989-06-15"),
        "encrypted" : False,
        "created" : parser.parse("1989-06-15"),
        "content" : "new to python tests\n",
        "title" : "How to get in touch with mocks",
        "categories" : [ "docs" ],
        "tags" : [ "python", "mock", "tests" ] })
    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce7bdb587"),
        "updated" : parser.parse("2016-03-05"),
        "encrypted" : True,
        "created" : parser.parse("2016-03-05"),
        # plaintext: "pynacl is just great"
        "content" : "8d55029288e4421b1770c1335f8d1de433b6615106cf1c709c9d73f6b45c2bef2a7d4d6766615a1742e987d458441a69f7ac85750c22781a088eb199",
        "title" : "This is an encrypted entry",
        "categories" : [ "crypto" ],
        "tags" : [ "pyblake2", "crypto" ] })
    c = mongomock.MongoClient().db.collection

    for doc in docs:
        c.insert(doc)
    return c

def mock_shortids_collection():

    docs = []

    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce8bdb583"),
        "oid" : ObjectId("569e5eed6815b47ce7bdb583"),
        "sid": 1},
        )
    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce8bdb584"),
        "oid" : ObjectId("569e5eed6815b47ce7bdb584"),
        "sid": 2},
        )
    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce8bdb585"),
        "oid" : ObjectId("569e5eed6815b47ce7bdb585"),
        "sid": 3},
        )
    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce8bdb586"),
        "oid" : ObjectId("569e5eed6815b47ce7bdb586"),
        "sid": 4},
        )
    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce8bdb587"),
        "oid" : ObjectId("569e5eed6815b47ce7bdb587"),
        "sid": 5},
        )

    c = mongomock.MongoClient().db.collection

    for doc in docs:
        c.insert(doc)
    return c

def mock_config_collection():

    docs = []

    # pw is test123
    docs.append({
        "_id": ObjectId("569e5eed6815b47ce9bdb583"),
        "masterkey": "90312727630970024125495afc71b5e111f2f375a140fa8450e3fd1ec4e947260ab22e960f5b32f75647bbb4ead88d42834c3099232fd8e10fe8838e56e5147e8a87dcfb251676a1",
        })

    c = mongomock.MongoClient().db.collection

    for doc in docs:
        c.insert(doc)
    return c


def mock_transactions_collection():

    docs = []

    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce1bdb583"),
        "document" : "569e5eed6815b47ce7bdb583",
        "date": parser.parse("2016-02-01"),
        "type": "edit",
        "title": "Nutella, Coffee, ninja",
        })
    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce1bdb584"),
        "document": "569e5eed6815b47ce7bdb583",
        "date": parser.parse("2016-01-30"),
        "type": "add",
        "title": "Nutella, Coffee, ninja",
        })
    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce1bdb585"),
        "document" : "569e5eed6815b47ce7bdb585",
        "date": parser.parse("2016-01-30"),
        "type": "show",
        "title": "Whoop Whoop Reloaded",
        })
    docs.append({
        "_id" : ObjectId("569e5eed6815b47ce1bdb586"),
        "document" : ObjectId("569e5eed6815b47ce7bdb586"),
        "date": parser.parse("2016-01-30"),
        "type": "delete",
        "title": "How to get in touch with mocks",
        })

    c = mongomock.MongoClient().db.collection

    for doc in docs:
        c.insert(doc)
    return c

def mock_editor(editor, template=""):
    template = template + "TEST"
    return template, "/tmp/THISNEVERMATCHES"

def mock_config():
    f = {
        'mailfrom': 'user@example.net',
        'shortids': 'cache',
        'transactions': 'transactions',
        'config': 'config',
        'db': 'rvo',
        'uri': 'mongodb://user:pass@localhost/rvo',
        'collection': 'documents',
        'editor': 'vim',
        'pager': 'vim -R'
    }
    return f

def normalize_element_without_regex(filter, field):
    """
    mongomock does not support regex...
    """
    if len(filter) > 0:
        filters = {field: { "$in": filter}}
    else:
        filters = {}

    print filters
    return filters

# Monkeypatch the shit out of rvo
@pytest.fixture(autouse=True)
def get_document_collection(monkeypatch):
    monkeypatch.setattr(rvo.db, "get_document_collection", mock_documents_collection)

@pytest.fixture(autouse=True)
def get_shortids_collection(monkeypatch):
    monkeypatch.setattr(rvo.db, "get_shortids_collection", mock_shortids_collection)

@pytest.fixture(autouse=True)
def get_config_collection(monkeypatch):
    monkeypatch.setattr(rvo.db, "get_config_collection", mock_config_collection)

@pytest.fixture(autouse=True)
def get_transactions_collection(monkeypatch):
    monkeypatch.setattr(rvo.db, "get_transactions_collection", mock_transactions_collection)

@pytest.fixture(autouse=True)
def get_editor(monkeypatch):
    monkeypatch.setattr(rvo.utils, "get_content_from_editor", mock_editor)

@pytest.fixture(autouse=True)
def get_config(monkeypatch):
    monkeypatch.setattr(rvo.config, "parse_config", mock_config)

@pytest.fixture()
def isatty_false(monkeypatch):
    monkeypatch.setattr(rvo.utils, "isatty", False)

@pytest.fixture()
def isatty_true(monkeypatch):
    monkeypatch.setattr(rvo.utils, "isatty", True)

@pytest.fixture()
def validation_item():
    item = {
       "content" : "Content",
       "created": datetime.datetime.now(),
       "updated": datetime.datetime.now(),
       "tags": [ "mongodb", "markdown" ],
       "categories": ["notes"],
       "encrypted": False,
       "title": "My very first entry",
    }
    return item


@pytest.fixture()
def mock_datetime_today(monkeypatch):
    monkeypatch.setattr(datetime.datetime, "now", datetime(2016, 4, 11, 17, 6, 14, 121180))

@pytest.fixture(autouse=True)
def mock_normalize_element(monkeypatch):
    monkeypatch.setattr(rvo.utils, "normalize_element", normalize_element_without_regex)

# Reusable functions from within tests.
def rvo_output(options, output):
    runner = CliRunner()
    print options
    result = runner.invoke(cli=cli.cli, args=options)
    print result
    for out in output:
        assert out in result.output
    assert result.exit_code == 0
    assert not result.exception

def rvo_err(options):
    runner = CliRunner()
    result = runner.invoke(cli.cli, options)
    assert result.exit_code == 1
    assert result.exception

