from flask import Flask, render_template, jsonify, redirect
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
import numpy as np
import pandas as pd
import datetime as dt
import pandas as pd
import json
import pprint

# Reflect Tables into SQLAlchemy ORM

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import sqlite3

# Connecting to the relational database
## Source: sqlite database from Kaggle Website

# Path to sqlite
database_path = "../Data/wdi_kaggle.sqlite"
engine = create_engine(f"sqlite:///{database_path}")
conn=engine.connect()

#get table names from database
for table_name in inspect(engine).get_table_names():
   print(table_name)

## Tables and exporting them to a Pandas DataFrame

Country_df=pd.read_sql('SELECT CountryCode, Region, IncomeGroup FROM Country',conn)
Indicators_df=pd.read_sql('SELECT * FROM Indicators',conn)
Series_df=pd.read_sql('SELECT SeriesCode, Topic, LongDefinition, AggregationMethod, LimitationsAndExceptions, Source, StatisticalConceptAndMethodology FROM Series',conn)

#### We realized that there are two codes (IndicatorCode in Indicator table and SeriesCode in Series table). 
# We needed to confirm that these two codes are exactly the same and that there is no difference between them (i.e., diff_Ind_Series is Null), 
# then we merge Series and Indicator tables based on this common column.

#find number of indicator and series codes
Indicators_df["IndicatorCode"].nunique()
Series_df["SeriesCode"].nunique()

#confirm that there are no differences between indicator and series codes from both tables
series = set(Series_df.SeriesCode)
diff_Ind_Series = [x for x in Indicators_df.IndicatorCode if x not in series]
diff_Ind_Series

### Now, we merge three DataFrames
Ind_Country=Indicators_df.merge(Country_df, left_on='CountryCode', right_on='CountryCode')
Ind_Country_Series=Ind_Country.merge(Series_df, left_on='IndicatorCode', right_on='SeriesCode')

####### Other option: Indictors = engine.execute('SELECT * FROM Indicators join Country on Indicators.CountryCode=Country.CountryCode').fetchall()

Ind_Country_Series.drop(['SeriesCode'],axis=1)

## Move DataFrame to Mongo DB

#### First, we tried to directly send the dataframe as a dictionary to the Mongodb. However, we faced the memory issure (MemoryError below). 
# So, we decided to turn the original Pandas Dataframe into 'ns' chuncks and feed them to the Mongodb

#change pandas dataframe to dictionary
Ind_Country_Series.to_dict("records")

#connect to mongodb database

#app = Flask(__name__)
#mongo = PyMongo(app, uri="mongodb://localhost:27017/WDI")

client = MongoClient('mongodb://localhost:27017/')
dbmongo = client.World_Development_Indicator

fn=0
ln=len(Ind_Country_Series)

# import to Mongo DB in chunks 

Ind_Country_Series_section=Ind_Country_Series[fn:ln]
nc=100

def chunk(df,x):
    return [ df[i::x] for i in range(x) ]
 
chunks = chunk(Ind_Country_Series_section, nc)

col=dbmongo['WDI_general']

#b=col.insert_many(chunks[x].to_dict(orient='records') for x in range(nc))
for count,x in enumerate(range(nc)):
    a=chunks[x].to_dict(orient='records') 
    col.insert_many(a)
    print(f"chunk={count}")

### At this point, we concluded that thte Jupyter notebook cannot export the very large size dataframe into the Mongodb.
#  Rather, we started transferring the whole code into a explicit Python file (Scrape_WDI.py).

## Extracting and Transforming from second Data Source

# Storing filepath in a variable
second_data = "../Data/API_EN.csv"

# Reading the data
second_data_df = pd.read_csv(second_data, skiprows=4)
second_data_df.head()

# Dropping columns
new_table_df = second_data_df.drop(columns=['Unnamed: 63'])
new_table_df.head()

# Merging tables
result_one = pd.merge(Country_df, new_table_df, left_on='CountryCode', right_on="Country Code")
result_one.drop(columns="Country Code")

# Saving the result in json
import json
result_one_dict = json.loads(result_one.to_json()).values()

## Loading second data in MongoDB
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Defining the database  and in Mongo
db = client.World_Development_Indicator
# Declaring the collection
carbon_dioxide_col = db.carbon_dioxide

# Inserting data
carbon_dioxide_col.insert_many(result_one.to_dict('records'))
client.close()

