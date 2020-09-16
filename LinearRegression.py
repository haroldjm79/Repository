###########  Machine Learning Linear Regression #####################
import pyspark
from pyspark.sql import SparkSession,SQLContext
from pyspark.ml.regression import LinearRegression
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler,StringIndexer
spark = SparkSession.builder.appName('hmodel').getOrCreate()
data = spark.read.csv('cruise_ship_info.csv',inferSchema=True,header=True)
data.show(5)
+-----------+-----------+---+------------------+----------+------+------+-----------------+----+
|  Ship_name|Cruise_line|Age|           Tonnage|passengers|length|cabins|passenger_density|crew|
+-----------+-----------+---+------------------+----------+------+------+-----------------+----+
|    Journey|    Azamara|  6|30.276999999999997|      6.94|  5.94|  3.55|            42.64|3.55|
|      Quest|    Azamara|  6|30.276999999999997|      6.94|  5.94|  3.55|            42.64|3.55|
|Celebration|   Carnival| 26|            47.262|     14.86|  7.22|  7.43|             31.8| 6.7|
|   Conquest|   Carnival| 11|             110.0|     29.74|  9.53| 14.88|            36.99|19.1|
|    Destiny|   Carnival| 17|           101.353|     26.42|  8.92| 13.21|            38.36|10.0|
+-----------+-----------+---+------------------+----------+------+------+-----------------+----+


for x in data.head(5):
    print(x,'\n')

data.groupBy('Cruise_line').count().show()


ndxr = StringIndexer(inputCol='Cruise_line',outputCol='cruise_ct')
ndxd = ndxr.fit(data).transform(data)

ndxd.head(3)
ndxd.show(5)
+-----------+-----------+---+------------------+----------+------+------+-----------------+----+---------+
|  Ship_name|Cruise_line|Age|           Tonnage|passengers|length|cabins|passenger_density|crew|cruise_ct|
+-----------+-----------+---+------------------+----------+------+------+-----------------+----+---------+
|    Journey|    Azamara|  6|30.276999999999997|      6.94|  5.94|  3.55|            42.64|3.55|     16.0|
|      Quest|    Azamara|  6|30.276999999999997|      6.94|  5.94|  3.55|            42.64|3.55|     16.0|
|Celebration|   Carnival| 26|            47.262|     14.86|  7.22|  7.43|             31.8| 6.7|      1.0|
|   Conquest|   Carnival| 11|             110.0|     29.74|  9.53| 14.88|            36.99|19.1|      1.0|
|    Destiny|   Carnival| 17|           101.353|     26.42|  8.92| 13.21|            38.36|10.0|      1.0|
+-----------+-----------+---+------------------+----------+------+------+-----------------+----+---------+
only showing top 5 rows

ndata = VectorAssembler(inputCols=['Age','Tonnage','passengers','length','cabins','passenger_density','cruise_ct']
                        ,outputCol='features')
tdata = ndata.transform(ndxd)
tdata.show(5)
+-----------+-----------+---+------------------+----------+------+------+-----------------+----+---------+--------------------+
|  Ship_name|Cruise_line|Age|           Tonnage|passengers|length|cabins|passenger_density|crew|cruise_ct|            features|
+-----------+-----------+---+------------------+----------+------+------+-----------------+----+---------+--------------------+
|    Journey|    Azamara|  6|30.276999999999997|      6.94|  5.94|  3.55|            42.64|3.55|     16.0|[6.0,30.276999999...|
|      Quest|    Azamara|  6|30.276999999999997|      6.94|  5.94|  3.55|            42.64|3.55|     16.0|[6.0,30.276999999...|
|Celebration|   Carnival| 26|            47.262|     14.86|  7.22|  7.43|             31.8| 6.7|      1.0|[26.0,47.262,14.8...|
|   Conquest|   Carnival| 11|             110.0|     29.74|  9.53| 14.88|            36.99|19.1|      1.0|[11.0,110.0,29.74...|
|    Destiny|   Carnival| 17|           101.353|     26.42|  8.92| 13.21|            38.36|10.0|      1.0|[17.0,101.353,26....|
+-----------+-----------+---+------------------+----------+------+------+-----------------+----+---------+--------------------+


fdata=tdata.select('features','crew')
fdata.show()
+--------------------+----+
|            features|crew|
+--------------------+----+
|[6.0,30.276999999...|3.55|
|[6.0,30.276999999...|3.55|
|[26.0,47.262,14.8...| 6.7|
|[11.0,110.0,29.74...|19.1|
|[17.0,101.353,26....|10.0|


train_data,test_data = fdata.randomSplit([0.7,0.3])
train_data.describe().show()
+-------+------------------+
|summary|              crew|
+-------+------------------+
|  count|               120|
|   mean| 7.893333333333344|
| stddev|3.6443220100816096|
|    min|              0.59|
|    max|              21.0|
+-------+------------------+

test_data.describe().show()
+-------+-----------------+
|summary|             crew|
+-------+-----------------+
|  count|               38|
|   mean|7.481052631578948|
| stddev|3.039066170116117|
|    min|             0.88|
|    max|             12.2|
+-------+-----------------+
ldata = LinearRegression(labelCol='crew')
model = ldata.fit(train_data)

trainmodel = model.evaluate(test_data)

trainmodel.meanAbsoluteError
#0.4271822926876402
trainmodel.meanSquaredError
#0.31291083300367645
trainmodel.r2
#0.9652045739163927
trainmodel.rootMeanSquaredError
#0.5593843338918927

trainmodel.residuals.show(5)
+-------------------+
|          residuals|
+-------------------+
|0.32159024900934163|
|   1.02626201363993|
|-0.2914326177981934|
|0.39089476558267755|
| 0.4192278037616699|


trainmodel.predictions.show(5)

+--------------------+----+------------------+
|            features|crew|        prediction|
+--------------------+----+------------------+
|[5.0,115.0,35.74,...|12.2|11.878409750990658|
|[5.0,122.0,28.5,1...| 6.7|  5.67373798636007|
|[6.0,112.0,38.0,9...|10.9|11.191432617798194|
|[6.0,113.0,37.82,...|12.0|11.609105234417322|
|[8.0,77.499,19.5,...| 9.0|  8.58077219623833|
+--------------------+----+------------------+