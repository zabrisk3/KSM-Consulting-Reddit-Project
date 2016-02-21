import numpy as np
import pandas as pd
from sklearn import svm
import matplotlib.pyplot as plt

""" This script Plots Linear SVM, RBF SVM, Polynomial (degree 2) SVM, and Polynomial (degree 3) SVM """

new_starwars_count = pd.read_excel('new_starwars_count.xlsx')

new_subreddit = pd.read_excel('new_subreddit.xlsx')



starwars=0
movies=0
for i in new_subreddit.index:
    if (str(new_subreddit['subreddit'][i]).lower() == 'starwars'):
        new_subreddit['subreddit'][i] = 1
        starwars+=1
    else:
        new_subreddit['subreddit'][i] = -1
        movies+=1

two_feature_dataframe = pd.concat([new_starwars_count['Titles'],new_starwars_count['Cast and Crew']], axis=1)


new_df = pd.DataFrame(new_subreddit['subreddit'].astype(int))
length = len(new_subreddit.index)
training_cut_off = int(length/3)
random_vector=np.arange(length)
np.random.shuffle(random_vector)

X = two_feature_dataframe.iloc[random_vector[0: training_cut_off-1]].as_matrix()  
y = np.ravel(new_df.iloc[random_vector[0: training_cut_off-1]].as_matrix())
h = 0.1


linear_svc = svm.SVC(kernel='linear').fit(X, y)
rbf_svc = svm.SVC(kernel='rbf').fit(X, y)
poly2_svc = svm.SVC(kernel='poly', degree=2).fit(X, y)
poly3_svc = svm.SVC(kernel='poly', degree=3).fit(X, y)

x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

titles = ['SVC with linear kernel',
          'SVC with RBF kernel',
          'SVC with polynomial (degree 2) kernel',
          'SVC with polynomial (degree 3) kernel']


for i, clf in enumerate((linear_svc, rbf_svc, poly2_svc, poly3_svc)):
    plt.subplot(2, 2, i + 1)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired)
    plt.xlabel('Film Titles')
    plt.ylabel('Cast and Crew')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())
    plt.title(titles[i])

plt.show()