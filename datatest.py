import torch




import sqlite3
import time
import pandas as pd
data = pd.read_csv('/Users/jorgebarahona/Downloads/croma_products_final.csv').dropna()
train_data = (data.name)
#
pname = data.name
#print(data.category.unique())
#exit()


# Create a Pandas DataFrame
df = pd.DataFrame(train_data)

# Connect to an SQLite database (creates a new one if it doesn't exist)
conn = sqlite3.connect("example.db")

TABLE_NAME = 'products'
# Create a table and dump the DataFrame data into the database
df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

# Query the database to confirm data insertion
query = f"SELECT * FROM {TABLE_NAME}"
result_df = pd.read_sql(query, conn)

# Display the data from the database
print("Data from the SQLite database:")
print(result_df)

# Close the database connection
conn.close()


