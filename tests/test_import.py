from conftest import rvo_output
from click.testing import CliRunner
from rvo import cli

def test_import():
    options = ['rimport']
    output = ['']
    rvo_output(options,output)
