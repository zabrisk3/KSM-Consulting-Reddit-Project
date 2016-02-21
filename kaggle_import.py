import pandas as pd
import sqlite3
"""Note: this Python code was run through Kaggle's website. It imports specific parts from the Reddit May 2015 data
and then saves it.

"""

sql_connect= sqlite3.connect('../input/database.sqlite')


"""Specify a desired number of rows to import and only import rows
whose subreddit is either "StarWars" or "movies". Order by id."""


n=55000



df = pd.read_sql('select "subreddit", "body" from May2015 where "subreddit" = "StarWars" or "subreddit"="movies" order by id limit '+ str(n),sql_connect)

""" Save """
writer = pd.ExcelWriter('StarWarsReddit.xlsx', engine='xlsxwriter')
df.to_excel(writer)
writer.save()
