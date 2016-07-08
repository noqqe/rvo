from conftest import rvo_output, rvo_err
from click.testing import CliRunner
from rvo import cli

def test_memories():
    options = ['memories', '-d', '2017-03-01']
    output = ["Whoop", "jrnl", "holiday", "vacation"]
    rvo_output(options,output)

