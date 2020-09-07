###########  Machine Learning Logistic Regression #####################
import pyspark
from pyspark.sql import SparkSession, SQLContext
spark = SparkSession.builder.appName('htest').getOrCreate()
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler,VectorIndexer,OneHotEncoder,StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator
hdata = spark.read.csv('products_h.csv',inferSchema=True,header=True)

hdata.show(5)
+---------+-------------+----------+----------+---------+------------+
|productid|  productname|supplierid|categoryid|unitprice|discontinued|
+---------+-------------+----------+----------+---------+------------+
|        1|Product HHYDP|         1|         1|     18.0|           0|
|        2|Product RECZE|         1|         1|     19.0|           0|
|        3|Product IMEHJ|         1|         2|     10.0|           0|
|        4|Product KSBRM|         2|         2|     22.0|           0|
|        5|Product EPEIM|         2|         2|    21.35|           1|

hdata.printSchema()
root
 |-- productid: integer (nullable = true)
 |-- productname: string (nullable = true)
 |-- supplierid: integer (nullable = true)
 |-- categoryid: integer (nullable = true)
 |-- unitprice: double (nullable = true)
 |-- discontinued: integer (nullable = true)
hdata.select(['productid','unitprice','categoryid','discontinued'])

df = hdata.select(['productid','unitprice','categoryid','discontinued'])

assembler = VectorAssembler(inputCols=['unitprice','categoryid','discontinued'],outputCol='features')

dflog = LogisticRegression(featuresCol='features',labelCol='productid')
pipeline = Pipeline(stages = [assembler,dflog])

dflog

train_data, test_data = df.randomSplit([0.7,0.3])
fit_model = pipeline.fit(train_data)
results = fit_model.transform(test_data)

val = BinaryClassificationEvaluator(rawPredictionCol='prediction',labelCol='productid')
results.select('productid','rawPrediction','prediction').show(5)
+---------+--------------------+----------+
|productid|       rawPrediction|prediction|
+---------+--------------------+----------+
|        1|[-1250837.5873916...|      76.0|
|        5|[-1986596.8900614...|      24.0|
|        8|[-1906735.9096122...|      63.0|
|       15|[-1601808.1293335...|      66.0|
|       16|[-2008163.5129995...|      50.0|
+---------+--------------------+----------+

