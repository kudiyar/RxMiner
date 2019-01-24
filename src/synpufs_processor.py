import os
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from functools import reduce  # For Python 3.x
from pyspark.sql import DataFrame

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.datastax.spark:spark-cassandra-connector_2.11:2.3.0 --conf spark.cassandra.connection.host=127.0.0.1 pyspark-shell'


def unionAll(*dfs):
    return reduce(DataFrame.unionAll, dfs)

def import_sample():
    sc = SparkContext.getOrCreate()
    sqlContext = SQLContext(sc)
    df_rxevent = sqlContext.read.format('csv').options(header='true', inferSchema='true').load('s3n://rxminer/SynPUFs/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_1.csv')
    df_bene1 = sqlContext.read.format('csv').options(header='true', inferSchema='true').load('s3n://rxminer/SynPUFs/DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv')
    df_bene2 = sqlContext.read.format('csv').options(header='true', inferSchema='true').load('s3n://rxminer/SynPUFs/DE1_0_2009_Beneficiary_Summary_File_Sample_1.csv')
    df_bene3 = sqlContext.read.format('csv').options(header='true', inferSchema='true').load('s3n://rxminer/SynPUFs/DE1_0_2010_Beneficiary_Summary_File_Sample_1.csv')
    df_carrier1 = sqlContext.read.format('csv').options(header='true', inferSchema='true').load('s3n://rxminer/SynPUFs/DE1_0_2008_to_2010_Carrier_Claims_Sample_1A.csv')
    df_carrier2 = sqlContext.read.format('csv').options(header='true', inferSchema='true').load('s3n://rxminer/SynPUFs/DE1_0_2008_to_2010_Carrier_Claims_Sample_1B.csv')
    df_inpat = sqlContext.read.format('csv').options(header='true', inferSchema='true').load('s3n://rxminer/SynPUFs/DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv')
    df_outpat = sqlContext.read.format('csv').options(header='true', inferSchema='true').load('s3n://rxminer/SynPUFs/DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv')
    df_npi = sqlContext.read.format('csv').options(header='true', inferSchema='true').load('s3n://rxminer/npi/npidata_pfile_20050523-20190113.csv')
    df_ndc = sqlContext.read.json('s3n://rxminer/openfda/drug-ndc-0001-of-0001.json')
    df_bene = unionAll(df_bene1, df_bene2, df_bene3)
    df_carrier = unionAll(df_carrier1, df_carrier2)

def link_synpufs():
    dr_rxevent.leftOuterJoin(df_bene1)

def load_and_get_table_df(keys_space_name, table_name):
    table_df = sqlContext.read\
        .format("org.apache.spark.sql.cassandra")\
        .options(table=table_name, keyspace=keys_space_name)\
        .load()
    return table_df

import_sample()

df.write\
    .format("org.apache.spark.sql.cassandra")\
    .mode('append')\
    .options(table="kv", keyspace="test")\
    .save()

df.show(10)