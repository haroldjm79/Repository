#pyspark basics
import findspark
findspark.init('/xxxx/xxxxxx/spark-2.1.1-bin-hadoop2.7')
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('hwins').getOrCreate()

df = spark.read.csv('appl_stock.csv',inferSchema=True,header=True)
df.printSchema()
df.head(3)

df.show(3)
df.filter('Close < 500').show()
df.filter('Close < 500').select('Open','Close').show()
df.filter(df['Close'] < 500).select('Volume').show()

df.filter((df['Close'] < 200) & (df['Open'] >200)).show()

df.filter((df['Close'] < 200) & ~(df['Open'] >200)).show() 
df.filter(df['Low'] == 197.16).show()
df.filter(df['Low'] == 197.16).collect()
result = df.filter(df['Low'] == 197.16).collect()
result
result[0]
row = result[0]
row.asDict()['Volume']

