from conftest import rvo_output, rvo_err
from click.testing import CliRunner
from rvo import cli

def test_modify_all_parameters():
    options = ['modify', '-t', 'foo', '-c', 'test', '569e5eed6815b47ce7bdb583']
    output = ['Updated', 'categories', 'test']
    rvo_output(options,output)

def test_modify_no_category():
    options = ['modify', '-t', 'footag', '-c', 'None', '569e5eed6815b47ce7bdb583']
    output = ['Updated', 'tags', 'footag']
    rvo_output(options,output)

def test_modify_no_tag():
    options = ['modify', '-t', 'None', '-c', 'foocat', '569e5eed6815b47ce7bdb583']
    output = ['Updated', 'categories', 'foocat']
    rvo_output(options,output)

def test_modify_two_cats():
    options = ['modify', '-t', 'foo', '-t', 'bar', '-c' ,'None', '569e5eed6815b47ce7bdb583']
    output = ['Updated', 'foo', 'bar']
    rvo_output(options,output)

def test_modify_no_cats_no_tags():
    options = ['modify', '569e5eed6815b47ce7bdb583']
    output = ['is already stored in plaintext']
    rvo_output(options,output)

def test_modify_two_cats():
    options = ['modify', '-t', 'None', '-c', 'foocat', '-c' ,'secondcat', '569e5eed6815b47ce7bdb583']
    output = ['Updated', 'categories', 'foocat']
    rvo_output(options,output)

def test_modify_no_parameters():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['modify', '569e5eed6815b47ce7bdb583'])
    assert not result.exception

def test_modify_no_parameters():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['modify', '569e5eed6815b47ce7bdb585'])
    assert not result.exception

def test_modify_shortid_all_parameters():
    options = ['modify', '-t', 'foo', '-c', 'test', '1']
    output = ['Updated', 'categories', 'test']
    rvo_output(options,output)

def test_modify_shortid_no_category():
    options = ['modify', '-t', 'footag', '-c', 'None', '1']
    output = ['Updated', 'tags', 'footag']
    rvo_output(options,output)

def test_modify_shortid_no_tag():
    options = ['modify', '-t', 'None', '-c', 'foocat', '1']
    output = ['Updated', 'categories', 'foocat']
    rvo_output(options,output)

def test_modify_shortid_two_cats():
    options = ['modify', '-t', 'foo', '-t', 'bar', '-c' ,'None', '1']
    output = ['Updated', 'foo', 'bar']
    rvo_output(options,output)

def test_modify_shortid_no_cats_no_tags():
    options = ['modify', '1']
    output = ['is already stored in plaintext']
    rvo_output(options,output)

def test_modify_shortid_two_cats():
    options = ['modify', '-t', 'None', '-c', 'foocat', '-c' ,'secondcat', '1']
    output = ['Updated', 'categories', 'foocat']
    rvo_output(options,output)

def test_modify_shortid_no_parameters():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['modify', '1'])
    assert not result.exception


def test_modify_encrypt_by_input_wrong_pw():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['modify', '-e', '1'], input="wrongpw\n")
    assert result.exception
    assert result.output.strip().endswith('Invalid Password')

def test_modify_encrypt_by_input():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['modify', '-e', '1'], input="test123\n")
    assert not result.exception
    assert result.output.strip().endswith('ninja is now stored encrypted')
