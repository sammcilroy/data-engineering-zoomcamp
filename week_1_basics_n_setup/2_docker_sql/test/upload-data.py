#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=100)
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
df.head()

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()

df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)

df = next(df_iter)
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

df.head(0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

while True:
    df = next(df_iter)
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')





