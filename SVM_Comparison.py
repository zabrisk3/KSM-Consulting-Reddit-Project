import numpy as np
import pandas as pd
from sklearn import svm
import math
from scipy.special import stdtr

""" This script runs Linear SVM, RBF SVM, Polynomial (degree 2) SVM, and Polynomial (degree 3) SVM
 10000 times each, it determines the average accuracy of each method, and then performs a t test to compare
 the averages.
 """

n=10000

new_starwars_count = pd.read_excel('new_starwars_count.xlsx')

new_subreddit = pd.read_excel('new_subreddit.xlsx')


for i in new_subreddit.index:
    if (str(new_subreddit['subreddit'][i]).lower() == 'starwars'):
        new_subreddit['subreddit'][i] = 1
    else:
        new_subreddit['subreddit'][i] = -1





new_df = pd.DataFrame(new_subreddit['subreddit'].astype(int))

linear_svc = svm.SVC(kernel='linear')
rbf_svc=svm.SVC(kernel='rbf')
poly2_svc=svm.SVC(kernel='poly', degree=2)
poly3_svc=svm.SVC(kernel='poly', degree=3)
length = len(new_subreddit.index)
training_cut_off = int(length/3)

svm_accuracy=[]
svm_standard_deviation=[]
svm_names=['Linear SVM','RBF SVM', 'Polynomial (Degree 2) SVM', 'Polynomial (Degree 3) SVM']
svm_types=[linear_svc, rbf_svc, poly2_svc, poly3_svc]
list_length=len(svm_types)

for clf in svm_types:
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


    average_accuracy=np.mean(np.array(total_accuracy))
    average_std=np.std(total_accuracy)
    svm_accuracy.append(average_accuracy)
    svm_standard_deviation.append(average_std)


ordered_accuracy=np.sort(np.array(svm_accuracy))
ordered_accuracy=ordered_accuracy[::-1]
ordered_indices=np.argsort(np.array(svm_accuracy))
ordered_indices=ordered_indices[::-1]


accuracy_df=pd.DataFrame({'1. SVM Method' : pd.Series([svm_names[ordered_indices[j]] for j in range(list_length)]),
                            '2. Average Accuracy': pd.Series([ordered_accuracy[j] for j in range(list_length)]),
                            '3. Accuracy Standard Deviation': pd.Series([svm_standard_deviation[ordered_indices[j]] for j in range(list_length)])
                            })

writer = pd.ExcelWriter('StarWars_DifferentSVMComparison.xlsx', engine='xlsxwriter')
accuracy_df.to_excel(writer)
writer.save()
print(accuracy_df)

t_test_df=pd.DataFrame({ "": pd.Series([accuracy_df['1. SVM Method'][j] for j in accuracy_df.index])})

for z in range(len(accuracy_df['1. SVM Method'])):
    df2=pd.DataFrame({ accuracy_df['1. SVM Method'][z]: [0.0 for k in accuracy_df.index] })
    t_test_df=pd.concat([t_test_df, df2], axis=1)

for m in accuracy_df.index:
    for i in range(m+1,len(accuracy_df.index)):
        mean1 = accuracy_df['2. Average Accuracy'][m]
        mean2 = accuracy_df['2. Average Accuracy'][i]
        N1= 10000
        N2= 10000
        sample_std1=accuracy_df['3. Accuracy Standard Deviation'][m]
        sample_variance1=(sample_std1)**2
        sample_std2=accuracy_df['3. Accuracy Standard Deviation'][i]
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
        print(t_test_df[t_test_df.columns.values[0]])
        t_test_df[t_test_df.columns.values[m+1]][i]=pf

writer = pd.ExcelWriter('accuracy_t_test.xlsx', engine='xlsxwriter')
t_test_df.to_excel(writer)
writer.save()