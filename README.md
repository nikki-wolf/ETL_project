STEPS:

Export: Started with a relational database (Sqlite) from a Kaggle project and the World Bank website

Transform: 
Data cleaning:
dropped some unnecessary columns and excluded some of the imported CSV files from the sqlite database followed by renaming some of the column headers.
Data transformation:
exported sqlite database into three Pandas dataframe where we could easily merge the tables. It was followed by exporting the dataframe into the Mongodb environment.¶

Note: we opt to apply Pandas DataFrame as a bridge between Sqlite and MongoDB to manipulate data. The other, and actually more professional approach, could be applied by the tools that are intended for this purpose, such as T3 Studio GUI.

Load: export data to a non-relational database (MongoDB)
