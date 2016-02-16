# KSM-Consulting-Reddit-Project
Introduction

Star Wars-themed posts can be found in different subreddits. These Python scripts perform classification. Collectively, they read in reddit bodies from two subreddits where Star Wars-themed posts can occur, "movies" and "StarWars", and attempts to classify whether or not the reddit body came from the "movies" subreddit or the "StarWars" subreddit based on the number of times words of certain Star Wars-themed categories appear in that body. In other words, it will attempt to classify based on scanning for certain types and certain frequencies of words in a reddit body. Being able to classifiy such reddit bodies in this way would be useful to Reddit if they were interested in designing algorithms for recommending other subreddits to current users. In this example, if someone makes Star Wars-themed posts under the "movies" subreddit, Reddit might recommend that they try the "Star Wars" subreddit. This might also be a benefit for targeted advertisements; as being able to classify a reddit body as "movies" or "Star Wars" could aid in what kind of ads to associate with a particular subreddit. Perhaps users whose bodies could be classified under the "movies" body more should be sent more advertisements about general movie offers (e.g. deals on theater chains), while users who post more under "Star Wars" could be sent more Star Wars-specific offers (e.g. discounts on Blue-rays). It also helps with identifying whether or not is meaningful to join certain subreddits together to form a new subreddit that might serve multiple interests. 

While this project is being used for Star Wars-themed reddit bodies, this can be extended to viritually any topic. For example, a similar classification concept could be implemented to group political posts, or to determine the most pertinent discussion topics amongst different politically affilitated subreddits. Another example would be in sports topics.  

The classification for this project is performed using Support Vector Machines, abbreviated as SVM. The reason for choosing SVM in order to classify data is that is provides a systematic and rigorous method for the classification; it can do so while also accounting for multiple variables; and it performs this classification relatively quickly. In essence, SVM views data as points in some n-dimensional space and attempts to separate data into destinct regions in that space. In this particular case, these regions will correspond to the two categories that the data falls into, "movies" or "Star Wars". There are multiple types of SVM, each approaching the problem of separation differently. Included in this github repository is a graph showing different types of SVM and how they separate two-dimensional data. 

For this project, a specific type of SVM is particularly useful: Linear SVM. Linear SVM, specifically, uses the method of attempting to find a hyperplane to separate data. An especially useful part of this approach is that it assigns special values, weights, to each dimension it works with (here the dimensions correspond to categories); the larger the magnitude of the weight, the more significant the category is to classification. This gives a key bearing on how important certain sets of words are to classification. From this, one can determine the most significant category in classifying these bodies. 

Results 

The results of performing 10000 iterations of both types of SVM can be seen. In the the excel table attached to this git hub, named.... Included in this table is the average accuracy of the classification, as well as a ranking of the categories based on the average value of the weights they were given. Also included is the standard deviation of the column. The average accuracy over the iterations was 71.43 The category with the highest weight was Cast and Crew, with the other categories having significantly lower weights. 

When considering the significance of certain categories, it's often help to look at variances or standard deviations to give some sense of how static the data is. An axiom data mining is that low variance or standard deviation for data is often indicative of comparatively less important information. When looking at the standard deviations presented in the table, it is true that the categories with the lowest weights also have lower standard deviations, suggesting a general trend between importance and standard deviation.. It's worth noting, though, that the category with lowest standard deviation, does not have the lowest weight; nor does the category with highest weight have the highest standard deviations. 

In particular, there are categories that have higher standard deviations but comparatively very low weights. This suggests that considering the numbers of words in these categories is not especially meaninguful for classification. 

With that in mind, considering how much greater the weight for Cast and Crew is then any other category, a route to proceed is to focus only on the words present in that category and how they influence classification. SVM could be run again to determine which word from this category is most important. 

However, to get a more direct and statistical bearing, it might be best to try rule mining in stead. 






