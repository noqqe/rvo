from conftest import rvo_output
from click.testing import CliRunner
from rvo import cli

def test_import():
    options = ['import']
    output = ['ninja', 'categories', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_import_encrypt():
    options = ['import', '-p', 'test123']
    output = ['ninja', 'pynacl', 'date', 'created', 'updated']
    rvo_output(options,output)


def test_import_encrypt_wrong_pw():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['import', '-p', 'wrongpw', ])
    assert result.output.strip().endswith('Invalid Password')
    assert result.exception

def test_import_json():
    options = ['import', '--from', 'json']
    output = ['ninja', 'categories', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_import_encrypt_json():
    options = ['import', '-p', 'test123', '--from', 'json']
    output = ['ninja', 'pynacl', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_import_markdown():
    options = ['import', '--from', 'markdown']
    output = ['broke', 'my', 'leg' ]
    rvo_output(options,output)

def test_import_encrypt_markdown():
    options = ['import', '-p', 'test123', '--from', 'markdown']
    output = ['broke', 'pynacl', 'leg' ]
    rvo_output(options,output)

def test_import_by_id():
    options = ['import', '--id', '3']
    output = ['Whoop', 'leg', 'again', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_import_by_category():
    options = ['import', '-c', 'docs']
    output = ['How', 'get', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_import_by_category():
    options = ['import', '-t', 'holiday']
    output = ['Whoop', 'leg', 'again', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_import_by_category_with_password():
    options = ['import', '-c', 'crypto', '-p', 'test123']
    output = ['pynacl', 'date', 'created', 'updated']
    rvo_output(options,output)

def test_import_by_id_encrypted():
    options = ['import', '--id', '5', '-p', 'test123']
    output = ['pynacl', 'date', 'created', 'updated']
    rvo_output(options,output)
