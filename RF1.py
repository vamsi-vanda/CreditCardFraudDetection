
from __future__ import print_function

from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint

import sys
import pandas as pd
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from pyspark.mllib.tree import RandomForest,RandomForestModel


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kafka_wordcount.py <zk> <topic>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="CreditFraud")
    sql_sc = SQLContext(sc)
    ssc = StreamingContext(sc, 1)

    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
#Giving the dstream to read as csv
    test_df = pd.read_csv(kvs)
    test_data = sql_sc.createDataFrame(test_df)
#Making RDD
    testdata = test_data.rdd.map(lambda row: LabeledPoint(row[-1], Vectors.dense(row[0:-1])))
    print("Number of test set rows: %d" % testdata.count())
    
#Loading the saved model
    saveModel = RandomForestModel.load(sc,"~/cdacproject/RFModel")
#checking accuracy
    predictions = saveModel.predict(testdata.map(lambda x: x.features))
    labels_and_predictions = testdata.map(lambda x: x.label).zip(predictions)
    acc = labels_and_predictions.filter(lambda x: x[0] == x[1]).count() / float(test_data.count())
    print("Model accuracy: %.3f%%" % (acc * 100))
    


    ssc.start()
    ssc.awaitTermination()
