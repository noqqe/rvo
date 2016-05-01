#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from conftest import rvo_output, rvo_err
from click.testing import CliRunner
from rvo import cli

def test_add_all_parameters(isatty_true):
    options = ['add', '-t', 'test', '-c', 'test', '--content', 'test']
    output = ['Document "test" created.']
    rvo_output(options,output)

def test_add_tags(isatty_true):
    options = ['add', '-t', 'test', '--content', 'test']
    output = ['Document "test" created.']
    rvo_output(options,output)

def test_add_title_test(isatty_true):
    options = ['add', '-t', 'test', '--content', 'THIS IS A TITLE']
    output = ['Document "THIS IS A TITLE" created.']
    rvo_output(options,output)

def test_add_title_test_gnarf(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-c', 'töstcät', '-x', 'gnarf'])
    assert not result.exception
    assert result.output.strip().endswith('Document "gnarf" created.')

def test_add_title_test_gnarf(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-c', 'töstcät', '-x', 'gnarf\nfoo'])
    assert not result.exception
    assert result.output.strip().endswith('Document "gnarf" created.')

def test_add_title_test_hashtag(isatty_true):
    options = ['add', '-t', 'test', '--content', '# THIS IS A TITLE']
    output = ['Document "THIS IS A TITLE" created.']
    rvo_output(options,output)

def test_add_title_test_hashtag(isatty_true):
    options = ['add', '-t', 'test', '--content', '# THIS IS A TITLE\nmutliline']
    output = ['Document "THIS IS A TITLE" created.']
    rvo_output(options,output)

def test_add_very_long_title(isatty_true):
    options = ['add', '-t', 'test', '--content', '# THIS IS A VERY VERY LONG NEVER ENDING TITLE THAT EXCEEDS LIMITS']
    output = ['Document "THIS IS A VERY VERY LONG NEVER ENDING TITLE THAT E" created.']
    rvo_output(options,output)

def test_add_no_parameters(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add'])
    assert result.output.strip().endswith('Document "TEST" created.')
    assert not result.exception

def test_add_one_parameters_tag(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-t', 'testtag'])
    assert result.output.strip().endswith('Document "TEST" created.')
    assert not result.exception

def test_add_utf8_cat(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-c', 'töstcät'])
    assert result.output.strip().endswith('Document "TEST" created.')
    assert not result.exception

def test_add_utf8_cat_multi(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-c', 'tüütüü', '-c', 'töstcät'])
    assert result.output.strip().endswith('Document "TEST" created.')
    assert not result.exception

def test_add_utf8_tag(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-t', 'töstcät'])
    assert result.output.strip().endswith('Document "TEST" created.')
    assert not result.exception

def test_add_utf8_tag_multi(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-t', 'tüütüü', '-t', 'töstcät'])
    assert result.output.strip().endswith('Document "TEST" created.')
    assert not result.exception

def test_add_encrypt_by_parameter_wrong_pw(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-e', '-p', 'thispasswordistotallywrong', '-t', 'encryption', '-c', 'test'])
    assert result.output.strip().endswith('Invalid Password')
    assert result.exception

def test_add_encrypt_by_parameter(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-e', '-p', 'test123', '-t', 'encryption', '-c', 'test'])
    assert result.output.strip().endswith('Document "TEST" created.')
    assert not result.exception

def test_add_encrypt_by_input(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-e', '-t', 'encryption', '-c', 'test'], input="test123\n")
    assert result.output.strip().endswith('Document "TEST" created.')
    assert not result.exception

def test_add_encrypt_by_input_with_content(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-e', '-t', 'encryption', '-x', 'TEST', '-c', 'test'], input="test123\n")
    assert result.output.strip().endswith('Document "TEST" created.')
    assert not result.exception

def test_add_encrypt_by_input_wrong_pw(isatty_true):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-e', '-t', 'encryption', '-c', 'test'], input="test2123\n")
    assert result.output.strip().endswith('Invalid Password')
    assert result.exception

def test_add_read_from_stdin(isatty_false):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add'], input="Schwifty\nSchwifty..lol\nMorty\n\n")
    assert result.output.strip().endswith('Document "Schwifty" created.')
    assert not result.exception

def test_add_read_from_stdin_with_cat(isatty_false):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-c', 'test'], input="Schwifty\nSchwifty..lol\nMorty\n\n")
    assert result.output.strip().endswith('Document "Schwifty" created.')
    assert not result.exception

def test_add_read_from_stdin_with_tag(isatty_false):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-t', 'tag'], input="Schwifty\nSchwifty..lol\nMorty\n\n")
    assert not result.exception
    assert result.output.strip().endswith('Document "Schwifty" created.')

def test_add_conflicting_stdin_reading(isatty_false):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', '-e'], input="Schwifty\nSchwifty..lol\nMorty\n\n")
    assert result.exception
    assert result.output.strip().endswith('Invalid Password')
