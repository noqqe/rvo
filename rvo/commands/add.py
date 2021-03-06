import sys
import re
import click
import fileinput
import datetime
import rvo.config
import rvo.db as db
import rvo.views as views
import rvo.utils as utils
import rvo.transaction as transaction
from rvo.validate import validate, validate_date, validate_location
from rvo.crypto import crypto

@click.command(help="""
            Add a document. 'add' is made to be very intuitive and functional.
            You can add and set all fields of a document during creation.

            It also supports reading from stdin. Unless this isn't the case
            it will start up your configured editor.
            """)
@click.option('encrypt', '-e' ,'--encrypted', default=False, is_flag=True, help='Encrypt this document')
@click.option('tags', '-t' ,'--tag',
              type=str, required=False, show_default=False, multiple=True,
              help='Set tags for this document')
@click.option('categories', '-c' ,'--category',
              type=str, required=False, show_default=False, multiple=True,
              help='Set categories for this document')
@click.option('date', '-d', '--date', default=datetime.datetime.now(),
              help='Set a custom creation date for this document', callback=validate_date)
@click.option('location', '-l', '--location', default=None, required=False,
              help='Set a location for this document', callback=validate_location)
@click.option('password', '-p', '--password', required=False, default=False,
              help="Password for encrypted documents")
@click.option('content', '-x', '--content', default=False, required=False, help='Read content from parameter')
@click.pass_context
def add(ctx, date, tags, categories, location, content, password, encrypt):
    """
    Adds a new document with various meta data options.
    """

    config = ctx.obj["config"]

    # Kindly ask for password when encryption comes
    if encrypt:
        c = crypto(ctx, password)
        if not c:
            sys.exit(1)

    # If input from -x parameter, encode in utf8
    try:
        content = content.encode("utf8")
    except (AttributeError, UnicodeEncodeError):
        pass

    # Read content directly from stdin if:
    # * there is no content from -x
    # * document should not be encrypted (conflicts with password prompt)
    # * there is piped input
    if not content and not encrypt and not utils.isatty:
        content = ""
        for l in click.get_text_stream('stdin'):
                content = content + l
        if content == "":
            content = False

    # If there is still no content and there is an interactive terminal,
    # open the editor to get query
    if not content and utils.isatty:
        content, tmpfile = utils.get_content_from_editor(config["editor"])

    # If everything fails, fail silently and let the user know.
    if not content:
        utils.log_error("Could not get any content")
        sys.exit(1)

    # Generate title from content
    title = utils.get_title_from_content(content)

    # Remove emojis
    title = utils.remove_emojis(title)

    # Encrypt
    if encrypt is True:
        content = c.encrypt_content(content)

    # if content looks like a url, set category and fetch title
    if re.compile("^https?://").search(content.lower()) is not None:

        # remove whitespace from right side
        content = content.rstrip()

        # check for duplicates
        if db.check_for_duplicate(ctx, field="url", content=content) is True:
            utils.log_info("Duplicate found")

        # fetch title and set category
        title = utils.get_title_from_webpage(content)

        categories = ["links"]

    # location
    loc = {}
    if location is None:
        loc["address"] = None
        loc["lat"] = None
        loc["long"] = None
    else:
        loc["address"] = location.address
        loc["lat"] = location.latitude
        loc["long"] = location.longitude

    # build item to insert into collection
    item = {
        "title": title,
        "content": content,
        "tags": list(tags),
        "categories": list(categories),
        "created": date,
        "updated": date,
        "encrypted": encrypt,
        "location": loc,
    }

    # insert item if its valid
    if validate(item):
        coll = db.get_document_collection(ctx)
        docid = coll.insert_one(item).inserted_id

        transaction.log(ctx, str(docid), "add", title)
        utils.log_info("Document \"%s\" created." % title)

    else:
        utils.log_error("Validation of the updated object did not succeed")

    try:
        utils.clean_tmpfile(tmpfile)
    except UnboundLocalError:
        pass

    return True
