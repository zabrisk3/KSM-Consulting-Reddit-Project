# KSM-Consulting-Reddit-Project

Star Wars-themed posts can be found in different subreddits. This Python script
performs linear classification. It reads in reddit bodies from two subreddits where Star Wars-themed 
posts can occur, "movies" and "StarWars", and attempts to classify whether or not the reddit body came 
from the "movies" subreddit or the "StarWars" subreddit based on the number of times words of certain Star Wars-themed
categories appear in that body. The classification is done through Linear SVM. Linear SVM creates a linear classifier 
and assigns weights to each category; the larger the magnitude of the weight, the more significant the category 
is to classification. The main goal is to determine the most significant category in classifying these bodies. 

The output from this code will be two data tables: a data table showing different Star Wars categories 
and the number of times words from those categories appear in a reddit body; and a smaller data table at the end, 
showing the weights obtained from Linear SVM, and an overall proportion that was correctly classified through Linear SVM. 
The categories will be ranked according to weight, starting with the largest in magnitude.

This code was run through Kaggle and takes about 20 minutes to run on that site. Based on 55000 samples, it was found that the 
Cast and Crew Category was the most significant in classification (see StarWars_Weights_and_Accuracy). The accuracy of the classifier 
was approximately 65%, which is better than what would be expected from randomly guessing. Larger sample sizes may lead to a higher 
accuracy of the classifier. 
