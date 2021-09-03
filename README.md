# RiskIQ SA Toolkit

This project contains Python libraries, command line utilities, and
various scripts to aid RiskIQ solution architects in developing
custom scripts.


## Internal Only

Please note this package is *not intended for distribution to customers* - if you need to build something they can use directly, contact a project contributor for help. 


## Installation

### Repo Access
You must first obtain read access to this repo. Contact a contributor to get that setup.


### Setup a virtual environment
It's best to setup a Python [virtual environment](https://docs.python.org/3/tutorial/venv.html) for your project. Change to your project's working directory and run this command:

```
python3 -m venv venv
```

This will create a folder named `venv` in your project directory. To activate the new virtual environment, run:

```
source venv/bin/activate
```

### Install the toolkit with pip
We will use the standard Python package manager, pip, to install the toolkit into our virtual environment.
```
python3 -m pip install git+ssh://git@github.com/philcowger/riqsolutions@main#egg=riqsolutions
```

## Usage

### Run the CLI
The toolkit provides a command line interface (CLI) to help with essential tasks including API authentication. To use it, run the riqsolutions module directly:
```
python3 -m riqsolutions --help
```

### Configure API access
Use the toolkit to configure API keys and store them on your local filesystem. This reduces the risk of checking in sensitive authentication keys.
```
python3 -m riqsolutions configure
```
Follow the prompts to provide your API credentials. By default, the toolkit writes the credentials to a file in your user's home directory. For details, see:
```
python3 -m riqsolutions configure --help
```

### Use the Python library
This example shows how to use toolkit after configuring your API credentials with the default options:
```python
from riqsolutions.riskiqapi import GlobalInventory
from riqsolutions.cli import configure_api

gi = GlobalInventory()
configure_api(gi)

tags = gi.get_tags()

for tag in tags:
   print(tag['name'])
```

