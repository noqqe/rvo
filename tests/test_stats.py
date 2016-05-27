from conftest import rvo_output
from click.testing import CliRunner
from rvo import cli

def test_stats_encrypt_wrong_pw():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['stats', '-p', 'wrongpw', '-c', 'crypto'])
    assert result.output.strip().endswith('Invalid Password')
    assert result.exception

def test_stats_encrypt_tag():
    options = ['stats', '-p', 'test123', '-t', 'crypto']
    output = ['pynacl', 'great']
    rvo_output(options,output)

def test_stats_by_category_with_password():
    options = ['stats', '-c', 'crypto', '-p', 'test123']
    output = ['pynacl']
    rvo_output(options,output)

def test_stats_by_id_encrypted():
    options = ['stats', '--id', '5', '-p', 'test123']
    output = ['pynacl' ]
    rvo_output(options,output)
