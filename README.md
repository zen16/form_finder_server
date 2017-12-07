### Description

Simple HTTP server that handle POST-requests and return correct form template name.
More info in Task.docx file (russian).

### Environment setup

Scripts works with python3.6
To install required packages you need:
* Install pip [this file](https://pip.pypa.io/en/stable/installing/)
* Install and activate standalone virtualenv, if you need
* Install required packages:
    python -m pip install -r ./requirements/common.txt

### Modules

* find_form.py - main module. Start web-server and handle POST-requests
* formsDB.json - test DB (TinyDB). It contains templates of forms 
* test_post_requests.py - send test request (expects test DB data)
* create_tinydb.py - test DB creation script
* /requirements/common.txt - list of installed packages in requirements format 

## Usage

1. Start HTTP server on port 8081:
    	run "form_finder_server.py"
2. Make test POST-requests:
		run "test_post_requests.py"
