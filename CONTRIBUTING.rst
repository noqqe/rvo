.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Get Started!
------------

Ready to contribute? Here's how to set up `rvo` for local development.

1. Fork the `rvo` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/rvo.git

3. Install your local copy into a virtualenv. Assuming you have virtualenv installed, this is how you set up your fork for local development::

    $ cd rvo/
    $ mkvirtualenv rvo
    $ workon rvo
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

5. Run the test suite

Run the built-in unittest module in the rvo root directory::

    $ cd rvo/
    $ PYTHONPATH=. py.test --cov=rvo

6. Submit a pull request through the GitHub website.
