from conftest import rvo_output, rvo_err
from click.testing import CliRunner
from rvo import cli

def test_stats():
    options = ['stats']
    output = ['tags', 'words', 'chars']
    rvo_output(options,output)

