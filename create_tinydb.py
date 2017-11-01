#!/etc/bin/env python3

"""
This module creates sample of TinyDB for tests
"""

import os
import sys
from tinydb import TinyDB


db_path = os.path.join(os.path.dirname(sys.argv[0]), 'formsDB.json')
db = TinyDB(db_path)
db.purge()

db.insert({'name': 'Main Form',
           'user_name': 'TEXT',
           'order_date': 'DATE',
           'lead_email': 'EMAIL'
           })
db.insert({'name': 'My Form',
           'user_name': 'TEXT',
           'primary_phone': 'PHONE',
           'order_date': 'DATE'
           })
db.insert({'name': 'Small Form',
           'user_name': 'TEXT',
           'primary_phone': 'PHONE'
           })
db.insert({'name': 'Warehouse Form',
           'article': 'TEXT',
           'part_number': 'TEXT'
           })
db.insert({'name': 'Simple email list',
           'email': 'EMAIL'
           })

print(db.all())
