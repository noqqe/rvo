from conftest import rvo_output, rvo_err
from click.testing import CliRunner
from rvo import cli

def test_delete_yes():
    options = ['delete', '569e5eed6815b47ce7bdb583', '--yes']
    output = ["Removed"]
    rvo_output(options,output)

def test_delete_input_yes():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['delete', '569e5eed6815b47ce7bdb583'], input="y\n")
    assert not result.exception
    assert result.output.strip().endswith('Removed Nutella, Coffee, ninja')

def test_delete_input_no():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['delete', '569e5eed6815b47ce7bdb583'], input="n\n")
    assert not result.exception
    assert not result.output.strip().endswith('Removed Nutella, Coffee, ninja')

def test_delete_input_default():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['delete', '569e5eed6815b47ce7bdb583'], input="\n")
    assert not result.exception
    assert not result.output.strip().endswith('Removed Nutella, Coffee, ninja')

def test_delete_nonexistent():
    options = ['delete', '769e5eed6815b47ce7bdb583']
    rvo_err(options)

def test_delete_shortid_yes():
    options = ['delete', '2', '--yes']
    output = ["Removed"]
    rvo_output(options,output)

def test_delete_shortid_input_yes():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['delete', '1'], input="y\n")
    assert not result.exception
    assert result.output.strip().endswith('Removed Nutella, Coffee, ninja')

def test_delete_shortid_input_no():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['delete', '1'], input="n\n")
    assert not result.exception
    assert not result.output.strip().endswith('Removed Nutella, Coffee, ninja')

def test_delete_shortid_input_default():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['delete', '1'], input="\n")
    assert not result.exception
    assert not result.output.strip().endswith('Removed Nutella, Coffee, ninja')

def test_delete_shortid_nonexistent():
    options = ['delete', '7']
    rvo_err(options)
