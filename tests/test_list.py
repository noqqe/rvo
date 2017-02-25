from conftest import rvo_output, rvo_err
from click.testing import CliRunner

def test_list():
    options = ['list']
    output = ['Tags', 'Cats', 'ID', 'Title']
    rvo_output(options,output)

# def test_list_content():
#     options = ['list', '-x', 'Nutrlla']
#     output = ['Whoop']
#     rvo_output(options,output)

def test_list_title():
    options = ['list', '-s', 'Nutella']
    output = ['Nutella']
    rvo_output(options,output)

def test_list_categories():
    options = ['list', '-c', 'notes']
    output = ["notes"]
    rvo_output(options,output)

def test_list_categories_two():
    options = ['list', '-c', 'jrnl']
    output = ["Whoop", "Reloaded"]
    rvo_output(options,output)

def test_list_categories_two():
    options = ['list', '-c', 'jrnl', '-c', 'docs']
    output = ['jrnl', 'docs']
    rvo_output(options,output)

def test_list_limit_one():
    options = ['list', '-c', 'jrnl', '-c', 'docs', '-l', '1']
    output = ['jrnl', '1 out of 3 result']
    rvo_output(options,output)

def test_list_limit_overload():
    options = ['list', '-c', 'jrnl', '-c', 'docs', '-l', '300']
    output = ['jrnl', 'docs', '3 out of 3 result']
    rvo_output(options,output)

def test_list_tags():
    options = ['list', '-t', 'list']
    output = ["list"]
    rvo_output(options,output)

def test_list_tags_two():
    options = ['list', '-t', 'list', '-t', 'todo']
    output = ['todo', 'list']
    rvo_output(options,output)

def test_list_from_to_year():
    options = ['list', '--from', '2015', '--to', '2016']
    output = ['1 out of 1 result(s)', 'notes']
    rvo_output(options,output)

def test_list_from_year():
    options = ['list', '--from', '2014']
    output = ['3 out of 3 result(s)', 'jrnl']
    rvo_output(options,output)

def test_list_to_year():
    options = ['list', '--to', '2014']
    output = ['2 out of 2 result(s)', 'holiday', 'Reloaded']
    rvo_output(options,output)

def test_list_to_date():
    options = ['list', '--to', '2015-02-03']
    output = ['3 out of 3 result(s)', 'holiday', 'Reloaded']
    rvo_output(options,output)

def test_list_from_date():
    options = ['list', '--from', '2015-02-03']
    output = ['2 out of 2 result(s)', 'holiday', 'Reloaded']
    rvo_output(options,output)

def test_list_from_date():
    options = ['list', '--from', '2015-01-30', '--to', '2015-02-03']
    output = ['1 out of 1 result(s)', 'Nutella', 'Coffee']
    rvo_output(options,output)
