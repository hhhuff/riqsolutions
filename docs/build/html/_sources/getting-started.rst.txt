===============
Getting Started
===============


RiskIQ SA Toolkit
=================

This project contains Python libraries, command line utilities, and various scripts to aid RiskIQ solution architects in developing custom scripts.

.. note::
    **Internal Only**

    Please note this package is not intended for distribution to customers - if you need to build something they can use directly, contact a project contributor for help.


Installation
------------

Repo Access
^^^^^^^^^^^
You must first obtain read access to this repo. Contact a contributor to get that setup.


Setup a virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^
It's best to setup a Python `virtual environment <https://docs.python.org/3/library/venv.html>`_ for your project. Change to your project's working directory and run this command:

.. code-block:: python

    python3 -m venv venv

This will create a folder named `venv` in your project directory. To activate the new virtual environment, run:

.. code-block:: python

    source venv/bin/activate


Install the toolkit with pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We will use the standard Python package manager, pip, to install the toolkit into our virtual environment.

.. code-block:: python

    python3 -m pip install git+ssh://git@github.com/philcowger/riqsolutions@main#egg=riqsolutions

Or download the toolkit source: https://github.com/philcowger/riqsolutions/archive/refs/heads/master.zip and install from the local location

.. code-block:: python

    pip install /your/local/location/riqsolutions


Usage
-----


Configure API access
^^^^^^^^^^^^^^^^^^^^^^^^
Use the toolkit to configure API keys and store them on your local filesystem. This reduces the risk of checking in sensitive authentication keys.  You will need your API Token, API key, and a name to use for credentials context.

You can use the cli configure prompter to provide your credentials for a 'default' context:
(This will prompt you for an api_token and api_key only.  The context will be 'DEFAULT'.)

.. code-block:: python

    python3 -m riqsolutions configure


Or you can supply your initial configuration credentials to the configure function directly:

.. code-block:: python

    python3 -m riqsolutions configure --api_token={your_api_token} --api_key={your_api_key} --context={your_context_name}


To create additional credentials contexts for use with the library use the --update command with the configure function

.. code-block:: python

    python3 -m riqsolutions configure --api_token={your_api_token} --api_key={your_api_key} --context=roote --update


Follow the prompts to provide your API credentials. By default, the toolkit writes the credentials to a file in your user's home directory. For details, see:

.. code-block:: python

    python3 -m riqsolutions configure --help


Use the Python library
^^^^^^^^^^^^^^^^^^^^^^^^^^
This example shows how to use toolkit after configuring your API credentials with the default options:

.. code-block:: python

    from riqsolutions.riskiqapi import GlobalInventory
    from riqsolutions.cli import configure_api

    gi = GlobalInventory()
    configure_api(gi, context={your_context_name})

    tags = gi.get_tags()

    for tag in tags:
        print(tag['name'])

