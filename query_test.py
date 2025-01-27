
import sqlite3
import time
import pandas as pd
import requests

conn = sqlite3.connect("example.db")

TABLE_NAME = 'products'

res = conn.execute( f'select * from {TABLE_NAME}' )


rows = []
while not( (row:=res.fetchone()) is None ):
    rows.append( row[0] ) 

6
POST_PATH = 'http://localhost:8004/column'
print(requests.post( POST_PATH, json={
    "table_name": "products",
    "uid": [*range(len(rows))],
    "column_name": "name",
    "data": rows
} ).status_code)



