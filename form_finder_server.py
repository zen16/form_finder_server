#!/etc/bin/env python3

"""
This module start HTTP server and handle '/get_form' requests
"""

import sys
import os
import re
import urllib
import logging
import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from tinydb import TinyDB
from datetime import datetime


class FindFormHandler(BaseHTTPRequestHandler):
    def _set_headers(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        # Gets the size of data
        content_length_str = self.headers['Content-Length']
        if not content_length_str:
            return
        # Gets the data itself
        post_data = urllib.parse.parse_qsl(
            self.rfile.read(int(content_length_str)).decode()
        )

        if self.path == '/get_form':
            if post_data:
                self._set_headers(200)  # Status Code: OK
                logging.debug('Request: {}'.format(post_data))
                # Getting typified unique post data
                typified_post_data = {}
                for field_name, value in post_data:
                    typified_post_data[field_name] = get_field_type(value)

                best_form = find_best_form(typified_post_data, db)
                if best_form:
                    self.wfile.write(bytes(best_form, "utf8"))
                    logging.debug('Best form: {}'.format(best_form))
                else:
                    message = json.dumps(typified_post_data,
                                         sort_keys=True, indent=4,
                                         separators=(',', ': '))
                    self.wfile.write(bytes(message, "utf8"))
                    logging.debug('Type of field: {}'.format(message))
                return
            self._set_headers(400)  # Status Code: Bad Request
            return
        self._set_headers(501)  # Status Code: Not Implemented
        return


def validate_date(date):
    first_match = re.match(r'^(\d\d)\.(\d\d)\.(\d{4})$', date)
    if first_match:
        day, month, year = first_match.groups()
        str_date = '{}-{}-{}'.format(year, month, day)
    elif re.match(r'\d{4}-\d\d-\d\d$', date):
        str_date = date
    else:
        return False

    try:
        datetime.strptime(str_date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_field_type(value):
    if validate_date(value):
        return 'DATE'

    phone_pattern = re.compile(r'\+7( \d{3}){2}( \d{2}){2}$')
    if phone_pattern.match(value):
        return 'PHONE'

    email_pattern = re.compile(
        r"[\w\-.]+"
        r"@ [a-zA-Z0-9] ([-a-zA-Z0-9.]{0,61}[a-zA-Z0-9])? "
        r"\.[a-zA-Z]{2,}$",
        flags=re.X
        )
    if email_pattern.match(value):
        return 'EMAIL'

    # it's text!
    return 'TEXT'


def find_best_form(request_data, database):
    best_form = None
    best_len = 0
    for form_template in database.all():
        match_current = True
        for template_field, field_value in form_template.items():
            if template_field == 'name':
                continue
            if field_value != request_data.get(template_field):
                match_current = False
                break
        if match_current:
            if len(form_template) > best_len:
                best_form = form_template['name']
                best_len = len(form_template)

    return best_form


def run_server():
    print('starting server...')
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, FindFormHandler)
    print('running server...')
    httpd.serve_forever()


if __name__ == '__main__':

    # logging.basicConfig(level=logging.DEBUG)
    db_path = os.path.join(os.path.dirname(sys.argv[0]), 'formsDB.json')
    db = TinyDB(db_path)

    run_server()
