import torch




import sqlite3
import time
import pandas as pd
data = pd.read_csv('/Users/jorgebarahona/Downloads/croma_products_final.csv').dropna()
print(data.columns)

train_data = (data[['name', 'overview']])
#
#print(data.category.unique())
#exit()


# Create a Pandas DataFrame
df = pd.DataFrame(train_data)

# Connect to an SQLite database (creates a new one if it doesn't exist)
conn = sqlite3.connect("example.db")

TABLE_NAME = 'products'
# Create a table and dump the DataFrame data into the database
df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)


conn.close()


