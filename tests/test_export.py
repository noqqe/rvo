from conftest import rvo_output
from click.testing import CliRunner
from rvo import cli

def test_export():
    options = ['export']
    output = ['ninja', 'categories', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_export_encrypt():
    options = ['export', '-p', 'test123']
    output = ['ninja', 'pynacl', 'date', 'created', 'updated']
    rvo_output(options,output)


def test_export_encrypt_wrong_pw():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['export', '-p', 'wrongpw', ])
    assert result.output.strip().endswith('Invalid Password')
    assert result.exception

def test_export_json():
    options = ['export', '--to', 'json']
    output = ['ninja', 'categories', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_export_encrypt_json():
    options = ['export', '-p', 'test123', '--to', 'json']
    output = ['ninja', 'pynacl', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_export_markdown():
    options = ['export', '--to', 'markdown']
    output = ['broke', 'my', 'leg' ]
    rvo_output(options,output)

def test_export_encrypt_markdown():
    options = ['export', '-p', 'test123', '--to', 'markdown']
    output = ['broke', 'pynacl', 'leg' ]
    rvo_output(options,output)

def test_export_by_id():
    options = ['export', '--id', '3']
    output = ['Whoop', 'leg', 'again', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_export_by_category():
    options = ['export', '-c', 'docs']
    output = ['How', 'get', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_export_by_tag():
    options = ['export', '-t', 'holiday']
    output = ['Whoop', 'leg', 'again', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_export_by_category_with_password():
    options = ['export', '-c', 'crypto', '-p', 'test123']
    output = ['pynacl', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_export_by_id_encrypted():
    options = ['export', '--id', '5', '-p', 'test123']
    output = ['pynacl', 'date', 'created', 'updated']
    rvo_output(options,output)
