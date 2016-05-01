from conftest import rvo_output
from click.testing import CliRunner
from rvo import cli

def test_show():
    options = ['show', '569e5eed6815b47ce7bdb583']
    output = ['ninja']
    rvo_output(options,output)

def test_show_stdout():
    options = ['show', '--stdout', '569e5eed6815b47ce7bdb583']
    output = ['ninja']
    rvo_output(options,output)

def test_show_shortid():
    options = ['show', '1']
    output = ['ninja', 'Nutella']
    rvo_output(options,output)

def test_show_encrypt():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['show', '-p', 'test123', '5'])
    assert not result.exception
    assert result.output.strip().endswith('pynacl is just great')

def test_show_encrypt_wrong_pw():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['show', '-p', 'wrongpw', '5'])
    assert result.output.strip().endswith('Invalid Password')
    assert result.exception

def test_show_encrypt_by_input():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['show', '5'], input="test123\n")
    assert result.output.strip().endswith('pynacl is just great')
    assert not result.exception

def test_show_encrypt_by_input_wrong_pw():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['show', '5'], input="wrongpw\n")
    assert result.output.strip().endswith('Invalid Password')
    assert result.exception
