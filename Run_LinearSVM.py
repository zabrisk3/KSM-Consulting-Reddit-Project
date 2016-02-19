import numpy as np
import pandas as pd
from sklearn import svm
import matplotlib.pyplot as plt
import math
from scipy.special import stdtr

""" This script runs Linear SVM 10000 times and gives the statistics on accuracy and the SVM weights.  """
"""It also graphs the Avarege SVM Weight, the Weight Standard Deviation, and the Category Standard Deviation"""
"""It also performs a t test for the average magnitudes of the weights """

n=10000

new_starwars_count = pd.read_excel('new_starwars_count.xlsx')

new_subreddit = pd.read_excel('new_subreddit.xlsx')


starwars=0
movies=0
for i in new_subreddit.index:
    if (str(new_subreddit['subreddit'][i]).lower() == 'starwars'):
        new_subreddit['subreddit'][i] = 1
        starwars += 1
    else:
        new_subreddit['subreddit'][i] = -1
        movies += 1



new_df = pd.DataFrame(new_subreddit['subreddit'].astype(int))

clf = svm.SVC(kernel='linear')

length = len(new_subreddit.index)
training_cut_off = int(length/3)

coefficient_vector=[]
total_accuracy=[]

for i in range(n):
    random_vector=np.arange(length)
    np.random.shuffle(random_vector)
    training_input=new_starwars_count.iloc[random_vector[0: training_cut_off-1]].as_matrix()
    testing_input=new_starwars_count.iloc[random_vector[training_cut_off: length-1]].as_matrix()
    training_classes = new_df.iloc[random_vector[0: training_cut_off-1]].as_matrix()
    testing_classes	= new_df.iloc[random_vector[training_cut_off: length-1]].as_matrix() #
    training=np.ravel(training_classes)
    testing=np.ravel(testing_classes)
    clf.fit(training_input,training)
    predictions = clf.predict(testing_input)
    differences	= testing-predictions

    differences_count =	0
    array_length = len(testing_classes)

    for i in range(array_length):
	    if int(differences[i]) != 0:
		    differences_count += 1

    accuracy = 1-differences_count/array_length
    total_accuracy.append(accuracy)
    coefficient_vector.append(clf.coef_[0])

average_accuracy=np.mean(np.array(total_accuracy))

average_std=np.std(total_accuracy)
average_weights_vector=[]
weight_standard_deviations=[]
column_names=list(new_starwars_count.columns.values)
column_length=len(column_names)
for z in range(column_length):
    average_weights_vector.append(np.mean(np.array([coefficient_vector[y][z] for y in range(n)])))
    weight_standard_deviations.append(np.std(np.array([coefficient_vector[y][z] for y in range(n)])))

weight_values=np.sort(np.absolute(np.array(average_weights_vector)))
weight_values=weight_values[::-1]
weight_indices=np.argsort(np.absolute(np.array(average_weights_vector)))
weight_indices=weight_indices[::-1]


"""Create a new data frame with categories, weights, standard deviations, and
save as an Excel file."""


final_weights=pd.DataFrame({'1. Category' : pd.Series([column_names[weight_indices[j]] for j in range(column_length)]),
                            '2. Average Magnitude of Weight': pd.Series([weight_values[j] for j in range(column_length)]),
                            '3. Standard Deviation of Weight': pd.Series([weight_standard_deviations[weight_indices[j]] for j in range(column_length)]),
                            '4. Standard Deviation of Category': pd.Series([new_starwars_count[column_names[weight_indices[j]]].std() for j in range(column_length)])
                            })

writer = pd.ExcelWriter('StarWars_SVMLinearKernelWeights_Stats.xlsx', engine='xlsxwriter')
final_weights.to_excel(writer)
writer.save()
print(final_weights)

""" Create and save a dataframe for accuracy. """
accuracy_stats=pd.DataFrame({'1. Accuracy Mean': [average_accuracy],
                             '2. Accuracy Standard Deviation': [average_std],
                             '3. Proportion of Star Wars Subreddits': [starwars*1.0/(starwars+movies)],
                             '4. Proportion of Movies Subreddits' : [movies*1.0/(starwars+movies)]
                                })


writer = pd.ExcelWriter('StarWars_AccuracyStats.xlsx', engine='xlsxwriter')
accuracy_stats.to_excel(writer)
writer.save()
print(accuracy_stats)

""" Graph The average magnitude of the weights, the standard deviations of the weights, and the standard deviations of the categories """

dataframe=pd.DataFrame({ 'Average Magnitude of Weight': pd.Series([final_weights['2. Average Magnitude of Weight'][j] for j in final_weights.index]),
                         'Standard Deviation of Category' : pd.Series([final_weights['4. Standard Deviation of Category'][i] for i in final_weights.index]),
                         'Standard Deviation of Weight': pd.Series([final_weights['3. Standard Deviation of Weight'][i] for i in final_weights.index])
                         })

x_labels=[final_weights['1. Category'][j] for j in dataframe.index]

plt.figure(figsize=(12, 8))
bar_graph = dataframe.plot(kind='bar')
bar_graph.set_title("Weight Comparison")
bar_graph.set_xlabel("Category")
bar_graph.set_ylabel("")
bar_graph.set_xticklabels(x_labels)


plt.show()

""" Perform a t-test for the Average Magnitude of the Weights"""

t_test_df=pd.DataFrame({ "": pd.Series([final_weights['1. Category'][j] for j in final_weights.index])})

for z in range(len(final_weights['1. Category'])):
    df2=pd.DataFrame({ final_weights['1. Category'][z]: [0.0 for k in final_weights.index] })
    t_test_df=pd.concat([t_test_df, df2], axis=1)

for m in final_weights.index:

    for i in range(m+1,len(final_weights.index)):
        mean1 = final_weights['2. Average Magnitude of Weight'][m]
        mean2 = final_weights['2. Average Magnitude of Weight'][i]
        N1= n
        N2= n
        sample_std1=final_weights['3. Standard Deviation of Weight'][m]
        sample_variance1=(sample_std1)**2
        sample_std2=final_weights['3. Standard Deviation of Weight'][i]
        sample_variance2=(sample_std2)**2
        if mean1 > mean2:
            T_numerator=mean1-mean2

        else:
            T_numerator= mean2-mean1

        T_denominator=math.sqrt(sample_variance1/N1+sample_variance2/N2)

        T=T_numerator/T_denominator

        deg_fre_numerator = (sample_variance1/N1+sample_variance2/N2)**2
        deg_fre_denominator = (((sample_variance1)/N1)**2)/(N1-1)+(((sample_variance2)/N2)**2)/(N2-1)

        deg_fre=deg_fre_numerator/deg_fre_denominator
        pf = 2*stdtr(deg_fre, -np.abs(T))
        t_test_df[t_test_df.columns.values[m+1]][i]=pf

writer = pd.ExcelWriter('weights_t_test.xlsx', engine='xlsxwriter')
t_test_df.to_excel(writer)
writer.save()
