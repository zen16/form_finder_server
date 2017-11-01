#!/etc/bin/env python3

"""
This module send test requests to server.
Expect server use sample of TinyDB
"""

import requests
import json


def post_request(url_address, values):
    response = requests.post(url_address, data=values)
    try:
        response_text = json.loads(response.text)
    except json.JSONDecodeError:
        response_text = response.text
    return response.status_code, response_text


url = "http://127.0.0.1:8081/get_form"

# search algorithm checks
assert post_request(url, {'email': 'new@example.com'}) == \
       (200, 'Simple email list')
assert post_request(url, {'article': 's223366', 'part_number': '7ru58tyu'}) == \
       (200, 'Warehouse Form')

data = {'user_name': 'Mark', 'order_date': '30.11.2004',
        'lead_email': 'example@mail.com'}
assert post_request(url, data) == (200, 'Main Form')

data = {'user_name': 'Mark', 'order_date': '30.11.2004',
        'primary_phone': '+7 888 777 66 55',
        'lead_email': 'example@mail.com', 'count': 1}
assert post_request(url, data) == (200, 'Main Form')

data = {'user_name': 'Mark', 'order_date': '30.11.2004',
        'primary_phone': '+7 888 777 66 55', 'lead_email': 'example@mail.com'}
assert post_request(url, data) in ((200, 'Main Form'), (200, 'My Form'))


# date typing checks
assert post_request(url, {'date_of_birth': '1985-06-05'}) == \
       (200, {'date_of_birth': 'DATE'})
assert post_request(url, {'date_of_birth': '20.08.1985'}) == \
       (200, {'date_of_birth': 'DATE'})
assert post_request(url, {'date_of_birth': '29.02.2000'}) == \
       (200, {'date_of_birth': 'DATE'})
assert post_request(url, {'date_of_birth': '29.02.2001'}) == \
       (200, {'date_of_birth': 'TEXT'})
assert post_request(url, {'date_of_birth': 'a1985-06-05'}) == \
       (200, {'date_of_birth': 'TEXT'})
assert post_request(url, {'date_of_birth': '20.22.1985'}) == \
       (200, {'date_of_birth': 'TEXT'})
assert post_request(url, {'date_of_birth': '1985-06-32'}) == \
       (200, {'date_of_birth': 'TEXT'})


# other field typing checks
assert post_request(url, {'personal_phone': '+7 901 523 56 89'}) == \
       (200, {'personal_phone': 'PHONE'})
assert post_request(url, {'personal_phone': '+7 901 523-56-89'}) == \
       (200, {'personal_phone': 'TEXT'})
assert post_request(url, {'general_email': 'test@email.com'}) == \
       (200, {'general_email': 'EMAIL'})
assert post_request(url, {'general_email': 'example@test@email.com'}) == \
       (200, {'general_email': 'TEXT'})


# empty request
assert post_request(url, {}) == (400, '')

# incorrect url
assert post_request('http://127.0.0.1:8081/get_for',
                    {'user_name': 'Andrey'}) == (501, '')
assert post_request('http://127.0.0.1:8081',
                    {'user_name': 'Andrey'}) == (501, '')
