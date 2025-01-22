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



df = pd.DataFrame(train_data)

conn = sqlite3.connect("example.db")

TABLE_NAME = 'products'

df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
query = f"SELECT * FROM {TABLE_NAME}"
result_df = pd.read_sql(query, conn)


print(result_df)


conn.close()


