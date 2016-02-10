"""Star Wars themed posts can be found in different subreddits. This Python script
performs linear classification. It reads in reddit bodies from two subreddits, "movies" and "StarWars",
and attempts to classify whether or not the body came from the "movies" subreddit or
the "StarWars" subreddit based on the number of times words of certain categories appear in that body.
The classification is done through Linear SVM. Linear SVM creates a linear classifier
and assigns weights to each category; the larger the magnitude of the weight, the more significant
the category is to classification. The main goal is to determine the most significant category
in classifying these bodies. The output from this code will two data tables: a data table showing different Star Wars categories, and the number of times words from those categories appear in each body; and a smaller data table at the end, showing the weights obtained from Linear SVM, and an overall
proportion that was correctly classified through Linear SVM. The categories will be ranked according
to weight, starting with the highest weight."""

import numpy as np
import pandas as pd
from sklearn import svm
import sqlite3

"""Note: this Python code was run through Kaggle's website."""

sql_connect= sqlite3.connect('../input/database.sqlite')


"""Specify a desired number of rows to import and only import rows
whose subreddit is either "StarWars" or "movies". Order by id.
Note: 55000 rows will require this program to run for about 20 minutes if run on Kaggle's website."""

n=55000
df = pd.read_sql('select "subreddit", "body" from May2015 where "subreddit" = "StarWars" or "subreddit"="movies" order by id limit '+ str(n),sql_connect)
subreddit = pd.DataFrame(df['subreddit'])

"""In case n rows were not imported, redefine n to be the length of the dataframe."""

n=len(df.index)

"""Below are defined categories and keywords within those categories"""

starwars_keywords=pd.DataFrame({'Main Characters': pd.Series(['luke skywalker','obi-wan kenobi','han solo','chewbacca','darth vader','princess leia']),
                         'Planets': pd.Series(['tatooine','dagobah','hoth','coruscant','naboo','alderaan','cloud city','endor']),
                         'Secondary Characters': pd.Series(['r2-d2','c-3po','palpatine','yoda','jabba','lando','jar jar binks']),
                         'Plot Points': pd.Series(['the force','jedi','the dark side','the good side','sith']),
                         'Creatures': pd.Series(['jawa', 'womp rat','sarlacc','ewok','gungan','hutt','rancor','wookie',' droid']),
                         'Factions': pd.Series(['the republic','rebel','stormtrooper','clone','empire','separatist']),
                         'Ships and Weapons': pd.Series(['light saber','blaster','x-wing','tie fighter','at-at','at-st','death star','millennium falcon']),
                         'Cast and Crew': pd.Series(['mark hamill','harrison ford','carrie fisher','george lucas','alec guinness','john williams'])
                         })

"""The function below serves a dual purpose. First, it helps quickly
define a new dataframe in respect to another dataframe and also gives it
that dataframe's column names. Second, it help with reindexing
dataframes later on."""

def replace_column_name(m,dafr):
    new_df = pd.DataFrame(np.zeros((m,len(dafr.columns))))
    old_names = new_df.columns.values
    new_names = dafr.columns.values
    new_df.rename(columns = dict(list(zip(old_names, new_names))), inplace=True)
    return new_df

"""This will be the dataframe that holds information on how many times
a word from a certain category appeared in a reddit body. """

starwars_count = replace_column_name(n,starwars_keywords)

"""Count the number of times a word from a category appeared in a reddit body."""

for i in starwars_keywords.columns.values:
   for m in starwars_keywords[i]:
        for y,d in list(zip([x for x in range(n)], df['body'])):
            body = str(d).lower()
            word_count = body.count(str(m))
            starwars_count[i][y] += word_count

"""Unfortunately, most of the reddit bodies will not have any words from any categories.
Since the focus is on Star Wars subject matter, delete all rows containing only zeroes from the starwars_count dataframe,and delete those same rows in the subreddit dataframe."""

off_count = 0
for k in range(n):
    marker = 0
    for x in starwars_count.columns.values:
        if starwars_count[x][k] != 0:
            marker = 1
    if marker == 0:
        starwars_count = starwars_count.drop(starwars_count.index[k-off_count])
        subreddit=subreddit.drop(subreddit.index[k-off_count])
        off_count += 1

"""Having deleted rows, the indexing is currently a mess. To help out,
this will create new dataframes of the same size as the old ones.
These have all zeroes. """

new_starwars_count = replace_column_name(len(starwars_count.index),starwars_count)
new_subreddit = replace_column_name(len(subreddit.index),subreddit)

"""Define a new function to give the values from one dataframe to another."""

def replace_values(df1,df2):
    for e,f in list(zip(df1.index,df2.index)):
        for m in df1.columns:
            df1[m][e]=df2[m][f]
    return df1

"""Give new dataframes the values of the old ones."""

new_starwars_count = replace_values(new_starwars_count, starwars_count)
new_subreddit = replace_values(new_subreddit, subreddit)

""" Concatenate new_starwars_count and new_subreddit into a new
dataframe and save it as an Excel file."""

new_matrix=pd.concat([new_starwars_count,new_subreddit], axis=1)
writer = pd.ExcelWriter('StarWars.xlsx', engine='xlsxwriter')
new_matrix.to_excel(writer)
writer.save()
print(new_matrix)

"""Convert the values in new_subreddit to 1 for "StarWars" or 0 for "movies"."""

for i in new_subreddit.index:
    if (str(new_subreddit['subreddit'][i]).lower() == 'starwars'):
        new_subreddit['subreddit'][i] = 1
    else:
        new_subreddit['subreddit'][i] = 0

""""SVM specifically wants the values of new_subreddit designated as integers."""

new_df = pd.DataFrame(new_subreddit['subreddit'].astype(int))

"""Create a linear classifier."""
clf = svm.SVC(kernel='linear')

"""Use a randomly chosen third of the data for training and the rest for testing."""
length = len(new_subreddit.index)
training_cut_off =	int(length/3)
random_vector=np.arange(length)
np.random.shuffle(random_vector)
training_input=new_starwars_count.iloc[random_vector[0: training_cut_off-1]].as_matrix() #get first 10% for training
testing_input=new_starwars_count.iloc[random_vector[training_cut_off: length-1]].as_matrix() #Use remaining 90% for testing
training_classes = new_df.iloc[random_vector[0: training_cut_off-1]].as_matrix()# 25% Training classes
testing_classes	= new_df.iloc[random_vector[training_cut_off: length-1]].as_matrix() #

"""Fit the training data, predict on testing data, and get accuracy."""
clf.fit(training_input,training_classes)
predictions = clf.predict(testing_input)
differences	= testing_classes-predictions
differences_count =	0
array_length = len(testing_classes)

for i in range(array_length):
	if int(differences[i][0]) != 0:
		differences_count += 1

accuracy = 1-differences_count/array_length

"""Arrange the weights from SVM by magnitude."""

coefficient_vector = np.array(clf.coef_[0])
absolute_coefficient_vector = np.absolute(coefficient_vector)
weight_values=np.sort(absolute_coefficient_vector)
weight_values=weight_values[::-1]
weight_indices=np.argsort(absolute_coefficient_vector)
weight_indices=weight_indices[::-1]


"""Create a new dataframe with columns, weights, and accuracy and
save as an Excel file."""

column_names=list(new_starwars_count.columns.values)
accuracy_array=[]
accuracy_array.append(accuracy)
column_length=len(column_names)

for j in range(column_length-1):
    accuracy_array.append(" ")

final_weights=pd.DataFrame({'Category' : pd.Series([column_names[weight_indices[j]] for j in range(column_length)]),
                            'Linear Classifier Weights: Absolute Value': pd.Series([weight_values[j] for j in range(column_length)]),
                            'Linear Classifier Weights: Original': pd.Series([coefficient_vector[weight_indices[j]] for j in range(column_length)]),
                            'Overall Accuracy': pd.Series(accuracy_array)
                            })

writer = pd.ExcelWriter('StarWarsWeightsandAccuracy.xlsx', engine='xlsxwriter')
final_weights.to_excel(writer)
writer.save()
print(final_weights)