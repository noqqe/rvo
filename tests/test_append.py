from conftest import rvo_output, rvo_err
from click.testing import CliRunner
from rvo import cli

def test_append():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['append', '569e5eed6815b47ce7bdb583'], input="foo\n")
    assert not result.exception
    assert result.output.strip().endswith('Content appended to "Nutella, Coffee, ninja".')

def test_append_stdin():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['append', '569e5eed6815b47ce7bdb583'], input="foo\n")
    assert not result.exception
    assert result.output.strip().endswith('Content appended to "Nutella, Coffee, ninja".')

def test_append_content():
    options = ['append', '569e5eed6815b47ce7bdb583', '-x', 'APPEND']
    output = ['Content appended to "Nutella, Coffee, ninja".']
    rvo_output(options,output)

def test_append_content_encrypted():
    options = ['append', '569e5eed6815b47ce7bdb587', '-p', 'test123', '-x', 'APPEND']
    output = ['Content appended to "pynacl is just greatAPPEND".']
    rvo_output(options,output)

def test_append_content_long():
    options = ['append', '569e5eed6815b47ce7bdb583', '--content', 'APPEND']
    output = ['Content appended to "Nutella, Coffee, ninja".']
    rvo_output(options,output)

def test_append_input_none():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['append', '569e5eed6815b47ce7bdb583'], input="foo\n")
    assert not result.exception
    assert result.output.strip().endswith('Content appended to "Nutella, Coffee, ninja".')

def test_append_nonexistent():
    options = ['append', '769e5eed6815b47ce7bdb583']
    rvo_err(options)

def test_append_shortid_content():
    options = ['append', '-x', 'APPEND', '2']
    output = ['Content appended to "just broke my leg".']
    rvo_output(options,output)

def test_append_shortid_content_encrypted():
    options = ['append', '-p', 'test123', '-x', 'APPEND', '5']
    output = ['Content appended to "pynacl is just greatAPPEND".']
    rvo_output(options,output)

def test_append_shortid_content_long():
    options = ['append', '--content', 'APPEND', '2']
    output = ['Content appended to "just broke my leg".']
    rvo_output(options,output)

def test_append_shortid_stdin():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['append', '1'], input="foo\n")
    assert not result.exception
    assert result.output.strip().endswith('Content appended to "Nutella, Coffee, ninja".')

def test_append_shortid_nonexistent():
    options = ['append', '7']
    rvo_err(options)
