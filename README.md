# KSM-Consulting-Reddit-Project

Star Wars themed posts can be found in different subreddits. This Python script
performs Linear Classification using SVM. It reads in reddit bodies from two subreddits, "movies" and "StarWars",
and attempts to classify whether or not the body came from the "movies" subreddit or
the "StarWars" subreddit based on the number of times words of certain categories appear in that body.
The classification is done through Linear SVM. Linear SVM creates a Linear Classifier
and assigns weights to each category; the larger the magnitude of the weight, the more significant
the category is to classification. The main goal is to determine the most significant category
in classifying these reddit bodies. 

The output from this code will two data tables: a data table showing different Star Wars categories, 
and the number of times words from those categories appear in a reddit body; and a smaller data table at the end, 
showing the weights obtained from Linear SVM, and an overall proportion that was correctly classified through Linear SVM. 
The categories will be ranked according to weight, starting with the largest in magnitude.
