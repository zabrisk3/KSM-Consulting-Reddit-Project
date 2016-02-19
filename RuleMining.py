import pandas as pd
import numpy as np


new_subreddit = pd.read_excel('new_subreddit.xlsx')

""" This script performs basic rule mining using one-word rules. """

starwars=0.0
movies=0.0
for i in new_subreddit.index:
    if (str(new_subreddit['subreddit'][i]).lower() == 'starwars'):
        new_subreddit['subreddit'][i] = 1
        starwars+=1
    else:
        new_subreddit['subreddit'][i] = -1
        movies+=1

threshold=(starwars*1.0)/(starwars+movies)


df=pd.read_excel('Reddit_Body_Reduced.xlsx')

search_words= ['star wars','new hope','the empire strikes back','return of the jedi','phantom menace','attack of the clones','revenge of the sith','special edition','the force awakens','despecialized edition']

""" Level 1 """

word_search=pd.DataFrame({"": pd.Series(['Number of Movies Posts', 'Number of Star Wars Posts', 'Word Implies Movies', 'Word Implies Star Wars'])})

for e in range(len(search_words)):
    df2=pd.DataFrame({search_words[e]: [0.0,0.0,0.0,0.0]})
    word_search=pd.concat([word_search,df2],axis=1)


for m in search_words:
    movies_tally=0
    starwars_tally=0
    word_tally=0
    for i in df.index:
        body=str(df['body'][i]).lower()
        if body.count(str(m)) > 0:
            word_tally+=1
            if new_subreddit['subreddit'][i]== 1:
                starwars_tally +=1
            else:
                movies_tally +=1

    if word_tally > 0:
        word_search[str(m)][0]=movies_tally
        word_search[str(m)][1]=starwars_tally
        word_search[str(m)][2]=movies_tally/word_tally
        word_search[str(m)][3]=starwars_tally/word_tally


writer = pd.ExcelWriter('rule_mining_level_1.xlsx', engine='xlsxwriter')
word_search.to_excel(writer)
writer.save()


print(word_search)

good_rules=[[],[]]

for m in word_search.columns.values:
    if m !="":
        for i in range(2,4):
            if word_search[m][i]>threshold:
                good_rules[i-2].append(str(m))

print(good_rules)


""" Level 2 """

""" The following is a work-in-progress code for deriving two word rules. Unfortunately, time did
 not permit full implementation of this code.

 """
# name_pairs0=[]
# name_pairs0_dataframe=[]
#
# for m in range(len(good_rules[0])):
#     for j in range(m+1, len(good_rules[0])):
#         df2 = pd.DataFrame({good_rules[0][m]+" and " + good_rules[0][j]: [0.0, 0.0] })
#         name_pairs0.append([m,j])
#         name_pairs0_dataframe.append(df2)
#
#
# word_search0=name_pairs0_dataframe[0]
#
# for n in range(1,len(name_pairs0)):
#     word_search0=pd.concat([word_search0, name_pairs0_dataframe[n]], axis=1)
#
# for m in name_pairs0:
#     movies_tally=0
#     starwars_tally=0
#     word_tally=0
#     for i in df.index:
#         body=str(df['body']).lower()
#         if body.count(good_rules[0][m[0]])>0 and body.count(good_rules[0][m[1]]>0):
#             word_tally+=1
#             if new_subreddit['subreddit'][i]==1:
#                 starwars_tally+=1
#             else:
#                 movies_tally+=1
#     if word_tally >0:
#         word_search0[str(good_rules[0][m]+" and " + good_rules[0][j])][0]=(movies_tally*1.0)/word_tally
#         word_search0[str(good_rules[0][m]+" and " + good_rules[0][j])][1]=(starwars_tally*1.0)/word_tally
#
#
# print(word_search0)
#
#
# name_pairs1=[]
# name_pairs1_dataframe=[]
#
# for m in range(len(good_rules[1])):
#     for j in range(m+1, len(good_rules[1])):
#         df2 = pd.DataFrame({good_rules[1][m]+" and " + good_rules[1][j]: [0.0, 0.0] })
#         name_pairs1.append([m,j])
#         name_pairs1_dataframe.append(df2)
#
#
# word_search1=name_pairs1_dataframe[0]
#
# for n in range(1,len(name_pairs1)):
#     word_search1=pd.concat([word_search1, name_pairs1_dataframe[n]], axis=1)
#
# for m in name_pairs1:
#     movies_tally=0
#     starwars_tally=0
#     word_tally=0
#     for i in df.index:
#         body=str(df['body']).lower()
#         if (body.count(good_rules[1][m[0]])>0) and (body.count(good_rules[1][m[1]]>0)):
#             print('yes')
#             word_tally+=1
#             if new_subreddit['subreddit'][i]==1:
#                 starwars_tally+=1
#             else:
#                 movies_tally+=1
#     if word_tally >0:
#         word_search1[str(good_rules[1][m]+" and " + good_rules[1][j])][0]=(movies_tally*1.0)/word_tally
#         word_search1[str(good_rules[1][m]+" and " + good_rules[1][j])][1]=(starwars_tally*1.0)/word_tally
#
#
# print(word_search1)
