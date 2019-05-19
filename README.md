Topic: World Development Indicators

What?: Providing a database including several indicators that can be applied to analyze the objective of minimizing poverty globally as set by the World Bank.
 
Why?: These indicators are so diverse that a single database from one single webpage (database) cannot provide the required indications of movement toward the objective. So, we need to gather the database from several web pages each including some of the indicators.
 
How?: In order to track this objective, it is required to define several themes (as listed below) and within each category some indicators are set and measured. The indicators, however, can be shared within more than one category, for example, the global pattern in CO2 emission, or people access to primary infrastructures in each country. Then, the goal(s) of each category is (are) related to the primary objective of this project, i.e. measuring the global poverty line.
 
Introduction:
The World Development Indicators (WDI) is a compilation of relevant, high-quality, and internationally comparable statistics about global development and the fight against poverty. We explored several online resources to gain the required measurements pertaining to more than 1600 indicators for almost 220 economies, with some data series extending back more than 50 years. One of the import parameters that severely impacts the global indicators, is anthological carbon emission. Carbon dioxide emission is causing numerous problems around the world. With the issue of climate change far from resolved, understanding the determinants behind emission levels is necessary to improve forecasting and guide policy making. There is an evidence that emission factor depends on per capita income. Carbon dioxide table provides carbon dioxide emission data from 1960 till 2018 for every country around the world. This table can be used to see the correlation between carbon dioxide emission and income group levels in every country. 


STEPS in ETL project:

Export: 
Started with a relational database (Sqlite) including 7 large tables (>5.6 M rows) from a Kaggle project, 2 CSV files from the World Bank website together with scraping the World Bank websie.

Transform: 
Data cleaning:
Dropped some unnecessary columns and excluded some of the imported tables from the sqlite database followed by renaming some of the column headers. Then, we removed unnecessary columns within the selected tables.

Data transformation:
Exported sqlite database into three Pandas dataframes where we could easily merge the tables. It was followed by exporting the dataframe into the Mongodb environment.

Note: we opt to apply Pandas DataFrame as a bridge between Sqlite and MongoDB to manipulate data. The other, and actually more professional approach, could be applied by the tools that are intended for this purpose, such as T3 Studio GUI.

Load: export data (tweaked Kaggle tables, CSV files, and scraped tables from World Bank website) to a non-relational database (MongoDB).
Note: We ould NOT export the genrated but huge Panda dataframe into Mongodb from the Jupyter Notebook environment due to memory issue. As a result, we first sliced the database into 50 chunks and then used a python file (scrape_WDI.py).

To run the code:
1) connect to a mongodb server (in a terminal > mongod )
2) run the python file to generate the Mongo database and upload data to it (in a terminal > python scrape_WDI.py)
