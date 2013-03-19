# Normalized Searchengine Index Distance #
Normalized Searchengine Index Distance (NSID), also called Normalized Web Distance ([NWD](http://homepages.cwi.nl/~paulv/papers/crc08.pdf)), is a simple generalization of [Normalized Google Distance](http://en.wikipedia.org/wiki/Normalized_Google_distance) based on the paper [Automatic meaning discovery using Google [pdf]](http://homepages.cwi.nl/~paulv/papers/amdug.pdf). Normalized Google Distance is derived from Normalized Compression Distance, which is derived from Normalized Information Distance, which in turn is derived from the principles of Kolmogorov Complexity.

Machine learning techniques like random forests and SVM's are used to classify, cluster, auto-translate and more.

Searchengine Indexes supported at the moment are Hackernews search and Wikipedia search, but any sufficiently large searchengine index would suffice, provided it returns the number of results found for terms.

The collection of files here is to research NSID globally, and specifically how specialized searchengine indexes influence distances.

##randomforestclassifier.py##
###Description###
Predicts semantic relationships between a term and a trainingset, storing them in first-order logic. Currently trained to predict semantic relation to "colors", fed with data from the Hackernews Search API ([HN Search](https://www.hnsearch.com/api)).
###Dependancies###
urllib2, json, math, numpy, sklearn.
###Sample output###
	semantic_relation(crimson,colors)[0.23]
	semantic_relation(rose,colors)[0.21]
	semantic_relation(tangerine,colors)[0.41]
	semantic_relation(grey,colors)[0.78]
	semantic_relation(pastel,colors)[0.48]
	semantic_relation(design,colors)[0.08]
	semantic_relation(colors,colors)[0.83]
	semantic_relation(white,colors)[0.8]
	semantic_relation(contrast,colors)[0.5]
	semantic_relation(beige,colors)[0.32]
	semantic_relation(lilac,colors)[0.21]
