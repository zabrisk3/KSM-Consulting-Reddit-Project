import numpy as np
import pandas as pd


df=pd.read_excel('StarWarsRedditExcel.xlsx')
subreddit=pd.DataFrame(df['subreddit'])

n=len(df.index)

"""Below are defined categories and keywords within those categories that
this program will later search for."""

starwars_keywords=pd.DataFrame({'Main Characters': pd.Series(['luke skywalker','obi-wan kenobi','han solo','chewbacca','darth vader','princess leia','anakin']),
                         'Planets and Locations': pd.Series(['tatooine','dagobah','hoth','coruscant','naboo','alderaan','cloud city','endor','mos eisley','yavin']),
                         'Secondary Characters': pd.Series(['r2-d2','c-3po','palpatine','darth maul', 'sidious', 'dooku','yoda','boba fett','jabba','lando','jar jar binks','mace windu']),
                         'Plot Points': pd.Series(['the force','jedi','the dark side','the good side','sith','trench run']),
                         'Creatures': pd.Series(['jawa', 'womp rat','sarlacc','ewok','gungan',' hutt','rancor','wookie',' droid']),
                         'Titles': pd.Series(['star wars','new hope','the empire strikes back','return of the jedi','phantom menace','attack of the clones','revenge of the sith','special edition','the force awakens','despecialized edition']),
                         'Factions': pd.Series(['galactic senate','the republic','rebel','stormtrooper','clone trooper','empire','separatist']),
                         'Ships and Weapons': pd.Series(['light saber','blaster','x-wing','tie fighter','at-at','at-st','death star','millennium falcon']),
                         'Cast and Crew': pd.Series(['mark hamill','harrison ford','carrie fisher','george lucas','alec guinness','john williams','ewan mcgregor','hayden christensen','natalie portman'])
                         })
print(starwars_keywords)

"""The function below serves a dual purpose. First, it helps quickly
define a new data frame in respect to another data frame and also gives it
that data frame's column names. Second, it helps with reindexing
data frames later on."""

def replace_column_name(m,dafr):
    new_df = pd.DataFrame(np.zeros((m,len(dafr.columns))))
    old_names = new_df.columns.values
    new_names = dafr.columns.values
    new_df.rename(columns = dict(list(zip(old_names, new_names))), inplace=True)
    return new_df

"""This will be the data frame that holds a tally of how many times
a word from a certain category appeared in a reddit body. """

starwars_count = replace_column_name(n,starwars_keywords)

print(starwars_count.columns.values)
print(starwars_count.index)
"""Count the number of times a word from a category appeared in a reddit body."""

for i in starwars_keywords.columns.values:
    print(i)
    for y in df.index:
        for m in starwars_keywords[i]:
            if str(m).lower()=='nan':
                word_count = 0
            else:
                body = str(df['body'][y]).lower()
                word_count = body.count(str(m))
            starwars_count[i][y] += word_count
"""Most of the reddit bodies will not have any words from any categories.Delete all rows containing only zeroes
from the starwars_count data frame,and delete those same rows in the subreddit data frame."""

off_count = 0
for k in range(n):
    marker = 0
    for x in starwars_count.columns.values:
        if starwars_count[x][k] > 0:
            marker = 1
    if marker == 0:
        starwars_count = starwars_count.drop(starwars_count.index[k-off_count])
        subreddit=subreddit.drop(subreddit.index[k-off_count])
        df=df.drop(df.index[k-off_count])
        off_count += 1

writer = pd.ExcelWriter('new_df.xlsx', engine='xlsxwriter')
df.to_excel(writer)
writer.save()




new_starwars_count = replace_column_name(len(starwars_count.index),starwars_count)
new_subreddit = replace_column_name(len(subreddit.index),subreddit)
new_dataframe = replace_column_name(len(df.index),df)

"""Define a new function to give the values from one data frame to another."""

def replace_values(df1,df2):
    for e,f in list(zip(df1.index,df2.index)):
        for m in df1.columns:
            df1[m][e]=df2[m][f]
    return df1

"""Give new dataframes the values of the old ones. Save the dataframes"""

new_starwars_count = replace_values(new_starwars_count, starwars_count)
print(new_starwars_count)

writer = pd.ExcelWriter('new_starwars_count.xlsx', engine='xlsxwriter')
new_starwars_count.to_excel(writer)
writer.save()


new_subreddit = replace_values(new_subreddit, subreddit)
print(new_subreddit)

writer = pd.ExcelWriter('new_subreddit.xlsx', engine='xlsxwriter')
new_subreddit.to_excel(writer)
writer.save()


new_dataframe = replace_values(new_dataframe,df)
print(new_dataframe)
writer = pd.ExcelWriter('Reddit_Body_Reduced.xlsx', engine='xlsxwriter')
new_dataframe.to_excel(writer)
writer.save()



