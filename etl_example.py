#Simple Extract Transform Load example
import findspark
import pandas as pd
import numpy as np
import pymysql
import pyspark
from pyspark.sql import SparkSession, SQLContext
spark = SparkSession.builder.appName('etl').getOrCreate()
df = spark.read.csv('products_h.csv',inferSchema=True,header=True)
conn = pymysql.connect(database='hwins',user='xxxxxx', password = 'xxxxxxxx')
cursor = conn.cursor()

df.show(5)
+---------+-------------+----------+----------+---------+------------+
|productid|  productname|supplierid|categoryid|unitprice|discontinued|
+---------+-------------+----------+----------+---------+------------+
|        1|Product HHYDP|         1|         1|     18.0|           0|
|        2|Product RECZE|         1|         1|     19.0|           0|
|        3|Product IMEHJ|         1|         2|     10.0|           0|
|        4|Product KSBRM|         2|         2|     22.0|           0|
|        5|Product EPEIM|         2|         2|    21.35|           1|
+---------+-------------+----------+----------+---------+------------+
df.withColumn("tax",df['unitprice'] * .20).show(5)
tf = df.withColumn("tax",df['unitprice'] * .20)
tf.show(5)
tf.withColumn("AdjPrice",tf['unitprice'] + tf['tax']).show(5)
ndf = tf.withColumn("AdjPrice",tf['unitprice'] + tf['tax'])
+---------+-------------+----------+----------+---------+------------+------------------+--------+
|productid|  productname|supplierid|categoryid|unitprice|discontinued|               tax|AdjPrice|
+---------+-------------+----------+----------+---------+------------+------------------+--------+
|        1|Product HHYDP|         1|         1|     18.0|           0|               3.6|    21.6|
|        2|Product RECZE|         1|         1|     19.0|           0|3.8000000000000003|    22.8|
|        3|Product IMEHJ|         1|         2|     10.0|           0|               2.0|    12.0|
|        4|Product KSBRM|         2|         2|     22.0|           0|               4.4|    26.4|
|        5|Product EPEIM|         2|         2|    21.35|           1|4.2700000000000005|   25.62|
+---------+-------------+----------+----------+---------+------------+------------------+--------+
insert_query = 'Insert INTO Products (productid, productname, supplierid, categoryid, unitprice,discontinued, tax,Adjprice) VALUES'
insert_query

ndf.show(1)

ndf = ndf.toPandas()
ndf.head()
ndf.shape
ndf['productname']=('"'+ ndf['productname']+'"')
ndf.head()

for i in range(ndf.shape[0]):
    insert_query += '('
    
    for j in range(ndf.shape[1]):
        insert_query += str(ndf[ndf.columns.values[j]][i]) + ', '
        
    insert_query = insert_query[:-2] + '), '

insert_query = insert_query[:-2] + '; '
insert_query

cursor.execute(insert_query)

conn.commit()

