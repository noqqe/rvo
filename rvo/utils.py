import re
import sys
import os
import tempfile
import subprocess
import urllib2
import ssl
import click
from bs4 import BeautifulSoup

# Content utils

def get_content_from_editor(config, template=""):
    """
    Writes content to file and opens up the editor that is
    parameter config. Returns new content and deletes file
    :config: str (commands)
    :template: str
    :returns: bool
    """
    _, tmpfile = tempfile.mkstemp(prefix="rvo-", text=True, suffix=".md")
    with open(tmpfile, 'w') as f:
        if template:
            try:
                f.write(template.encode("utf-8"))
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                f.write(template)
    subprocess.call(config.split() + [tmpfile])
    with open(tmpfile, "r") as f:
        raw = f.read()
    if not raw:
        log_error("Error: No content from editor")
        sys.exit(1)
    return raw, tmpfile

def view_content_in_pager(config, template=""):
    """
    Writes content to file and opens up the pager that is
    parameter config. Temp file will be deleted afterwards.
    :config: str (commands)
    :template: str
    :returns: bool
    """
    _, tmpfile = tempfile.mkstemp(prefix="rvo-", text=True, suffix=".md")
    with open(tmpfile, 'w') as f:
        if template:
            try:
                f.write(template.encode("utf-8"))
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                f.write(template)
    subprocess.call(config.split() + ["+set nospell nonumber"] + [tmpfile])
    os.remove(tmpfile)
    return True

def get_title_from_webpage(url):
    """ Fetch <title> of a html site for title element
    :url: str (http url)
    :returns: str
    """

    # LOL SECURITY
    ssl._create_default_https_context = ssl._create_unverified_context

    try:
        h = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
        u = urllib2.Request(url, headers=h)
        u = urllib2.urlopen(u)
        soup = BeautifulSoup(u, "html.parser")
        s = soup.title.string.replace('\n', ' ').replace('\r', '').lstrip().rstrip()
        s = s.lstrip()
        return s
    except (AttributeError, MemoryError, ssl.CertificateError, IOError) as e:
        return "No title"
    except ValueError:
        return False

def get_title_from_content(content):
    """
    Generates a title from the content
    using the first line and stripping away whitespace
    and hash signs
    :content: str
    :returns: str

    """
    title = content.split('\n', 1)[0].replace('#', '').lstrip()[0:50]
    return title

def clean_tmpfile(tmpfile):
    """
    Basically, this removes a file. Its used to only
    delete the file that the editor leaves behind in case that
    rvo crashes.
    """
    try:
        os.remove(tmpfile)
    except OSError:
        pass
    return True

# Styling

query_prefix = '\033[38;5;154m>\033[38;5;118m>\033[38;5;120m>\033[0m'

def log_error(msg):
    """
    Error output on terminal
    """
    prefix = '\033[38;5;196m>\033[38;5;202m>\033[38;5;208m>\033[0m'
    click.echo(prefix + " " + msg)

def log_info(msg):
    """
    Info output on terminal
    """
    prefix = '\033[38;5;129m>\033[38;5;135m>\033[38;5;141m>\033[0m'
    click.echo(prefix + " " + msg)

# OS and Testing Utils

def isatty():
    """
    Wrapper for isatty
    I use this for monkeypatching input detection
    in the add method. Its not nice. It works. Its mine <3
    """
    return sys.stdin.isatty()

# Transformation of elements

def normalize_element(filter, field):
    """
    Turn items into a dict and apply regexes
    """

    if len(filter) > 0:
        filters = []
        for f in filter:
            filters.append(re.compile(f, re.IGNORECASE))
        filters = {field: { "$in": filters}}
    else:
        filters = {}

    return filters
