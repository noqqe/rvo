from conftest import rvo_output, rvo_err
from click.testing import CliRunner
from rvo import cli

def test_edit():
    options = ['edit', '569e5eed6815b47ce7bdb584']
    output = ['Document "just broke my leg" updated.']
    rvo_output(options,output)

def test_edit_shortid():
    options = ['edit', '2']
    output = ['Document "just broke my leg" updated.']
    rvo_output(options,output)

def test_edit_encrypt():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['edit', '-p', 'test123', '5'])
    assert not result.exception
    assert result.output.strip().endswith('Document "pynacl is just greatTEST" updated.')

def test_edit_encrypt_wrong_pw():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['edit', '-p', 'wrongpw', '5'])
    assert result.output.strip().endswith('Invalid Password')
    assert result.exception

def test_edit_encrypt_by_input():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['edit', '5'], input="test123\n")
    assert result.output.strip().endswith('Document "pynacl is just greatTEST" updated.')
    assert not result.exception

def test_edit_encrypt_by_input_wrong_pw():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['edit', '5'], input="wrongpw\n")
    assert result.output.strip().endswith('Invalid Password')
    assert result.exception
