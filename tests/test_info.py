from conftest import rvo_output, rvo_err

def test_info():
    options = ['info', '569e5eed6815b47ce7bdb583']
    output = ["list"]
    rvo_output(options,output)

def test_info_err():
    options = ['info', '769e5eed6815b47ce7bdb583']
    rvo_err(options)

def test_info_shortid():
    options = ['info', '1']
    output = ["list"]
    rvo_output(options,output)

def test_info_shortid_err():
    options = ['info', '7']
    rvo_err(options)
