from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
import numpy as np
import pandas as pd
import datetime as dt
import pandas as pd

# Reflect Tables into SQLAlchemy ORM
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import sqlite3

# Connecting to the relational database
# Source: sqlite database from Kaggle Website
# Path to sqlite
database_path = "Data/wdi_kaggle.sqlite"
engine = create_engine(f"sqlite:///{database_path}")
conn=engine.connect()
for table_name in inspect(engine).get_table_names():
   print(table_name)

# Tables and exporting them to a Pandas DataFrame
Country_df=pd.read_sql('SELECT CountryCode, Region, IncomeGroup FROM Country',conn)
Indicators_df=pd.read_sql('SELECT * FROM Indicators',conn)
Series_df=pd.read_sql('SELECT SeriesCode, Topic, LongDefinition, AggregationMethod, LimitationsAndExceptions, Source, StatisticalConceptAndMethodology FROM Series',conn)

#We realized that there are two codes (IndicatorCode in Indicator table and SeriesCode in Series table). 
# First, we confirm that these two codes are exactly the same since there is no difference between them 
# (i.e., diff_Ind_Series is Null), then we merge Series and Indicator tables based on this common column.
series = set(Series_df.SeriesCode)
diff_Ind_Series = [x for x in Indicators_df.IndicatorCode if x not in series]

# Now, we merge three DataFrames
Ind_Country=Indicators_df.merge(Country_df, left_on='CountryCode', right_on='CountryCode')
Ind_Country_Series=Ind_Country.merge(Series_df, left_on='IndicatorCode', right_on='SeriesCode')
Ind_Country_Series.drop(['SeriesCode'],axis=1)

# First, we tried to directly send the dataframe as a dictionary to the Mongodb. 
# However, we faced the memory issure (MemoryError below).
# So, we decided to turn the original Pandas Dataframe into 'ns' chuncks and feed them to the Mongodb
# IndCouSer.to_dict()

#app = Flask(__name__)
#mongo = PyMongo(app, uri="mongodb://localhost:27017/WDI")
client = MongoClient('mongodb://localhost:27017/')
dbmongo = client.World_Development_Indicator

fn=0
ln=len(Ind_Country_Series)

Ind_Country_Series_section=Ind_Country_Series[fn:ln]
nc=100

# import to Mongo DB in chunks 

def chunk(df,x):
    return [ df[i::x] for i in range(x) ]
 
chunks = chunk(Ind_Country_Series_section, nc)

col=dbmongo['WDI_general']

#b=col.insert_many(chunks[x].to_dict(orient='records') for x in range(nc))
for count,x in enumerate(range(nc)):
    a=chunks[x].to_dict(orient='records') 
    col.insert_many(a)
    print(f"chunk={count}")