from conftest import rvo_output, rvo_err
from click.testing import CliRunner
from rvo import cli

def test_log():
    options = ['log']
    output = ["ninja", "Whoop", "Type", "Title", "Nutella", "delete", "show"]
    rvo_output(options,output)

def test_log_limit_two():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['log', '-e', '1'])
    assert not result.exception
    assert result.output.strip().endswith('569e5eed6815b47ce1bdb583')

def test_log_limit_one():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['log', '-e', '2'])
    assert not result.exception
    assert 'edit' in result.output.strip()
    assert result.output.strip().endswith("569e5eed6815b47ce1bdb583")
