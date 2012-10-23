Installing gsapi
================

In order to install gsapi, you'll need the following packages 

* Flask
* Flask-PyMongo
* Flask-Testing
* mimerender
* simplejson
* bpython
* schematics
* rawes
* pyes
* pexpect
* pymongo
* fabric
* python-dateutil
* python 2.7

To make it run, you just have to do something like::

    cd into a python projects directory 
    git clone ......
    cd gsapi
    virtualenv venv

Create a local_settings to override for your environment

    cp settings.py local_settings.py

This is a windows hack to set some paths, etc. You may need to adjust for your Windows environment.

    activate.cmd

Non-Windows users:

    source venv/bin/activate
    cd gsapi

    pip install -r requirements.txt

Run tests:

    nosetests
    Or:
        nosetests -v
        nosetests -v -s
        nosetests -v -s --nocapture

Run the application:

    python run.py


Deploy it (Coming Soon!)
------------------------

To deploy it, I'm using gunicorn and supervisord::

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Also, create a `local_settings.py` file with the appropriate values to use a different database for instance.

Developer Notes
---------------

If you use WingWare IDE (Highly recommended), here are some useful settings for debugging:

Project/Project Settings

    Environment
        Python Path (Added):
            c:\Users\Larry\__prjs\_ex\_prjs\gsapi\venv\Lib\site-packages
            c:\Users\Larry\__prjs\_ex\_prjs\gsapi
    Debug
        Main Debug File:
            c:\Users\Larry\__prjs\_ex\_prjs\gsapi\gsapi\run.py
        Initial Directory:
            c:\Users\Larry\__prjs\_ex\_prjs\gsapi\gsapi
        Python Options (set testing ON, see gsapi.run.main)
            -t
    Testing
        Default Test Framework
            Nose

