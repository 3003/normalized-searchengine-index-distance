import urllib2
from json import loads
import math
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation

# HELPER
def fetch_data(source_url):
	request = urllib2.Request(source_url)
	try: 
		response = urllib2.urlopen(request)
		data = response.read()
		return (data, source_url)
	except urllib2.URLError, e:
		return (None, e)

def save_data(data, filename):
	fh = open(filename, "w")
	fh.write(data)

# FETCH AND PREP DATA
def get_hits(term):
	data = fetch_data("http://api.thriftdb.com/api.hnsearch.com/items/_search?q=" + term)
	if data[0] is not None:
		if loads(data[0])['hits'] > 0:
			return loads(data[0])['hits']
		else:
			return 0.000001
	else:
		return data[1]

# DISTANCE MEASURE		
def normalized_index_distance(nr_results_x, nr_results_y, nr_results_x_y, index_size = 11200000):
	c_x = math.log(nr_results_x)
	c_y = math.log(nr_results_y)
	c_x_y = math.log(nr_results_x_y)
	c_m = math.log(index_size)
	return (max(c_x, c_y) - c_x_y) / (c_m - min(c_x, c_y))

# CLASSIFYING
def build_classifier(training_set_location = 'data/mytrainingset.csv', classifier = 'RandomForestClassifier'):
	if classifier == 'RandomForestClassifier':
		classifier_object = RandomForestClassifier(n_estimators=100)
	dataset = np.genfromtxt(open(training_set_location,'r'), delimiter=',', dtype='f8')[1:]
	train = [x[1:] for x in dataset]
	target = [x[0] for x in dataset]
	classifier_object.fit(train, target)
	return classifier_object
	
def predict_class(classifier_object, data, result = 1):
	return float(classifier_object.predict_proba(data)[0][1])
	
# TRAINING, TESTING
def create_training_set(anchors, train_positive, train_negative, filename = 'data/mytrainingset.csv'):
	hits = {}
	for item in anchors + train_positive + train_negative:
		hits[item] = get_hits(item)
	csv = "Class"
	for anchor in anchors:
		csv = csv + "," + anchor
	csv = csv + "\n"
	for item in train_positive + train_negative:
		if item in train_positive:
			csv = csv + "1"
		else:
			csv = csv + "0"
		for anchor in anchors:
			print item, anchor
			csv = csv + "," + str(normalized_index_distance(hits[item], hits[anchor], get_hits(item + "+" + anchor)))
		csv = csv + "\n"
	save_data(csv, filename)
	
def create_test_set(anchors, test_cases, filename = 'data/mytestset.csv'):
	hits = {}
	csv = ""
	for item in test_cases + anchors:
		hits[item] = get_hits(item)
	print hits
	for anchor in anchors:
		csv = csv + anchor + ","
	csv = csv[:-1] + "\n"
	for item in test_cases:
		for anchor in anchors:
			print item, anchor
			csv = csv + str(normalized_index_distance(hits[item], hits[anchor], get_hits(item + "+" + anchor))) + ","
		csv = csv[:-1] + "\n"
	save_data(csv, filename)

def create_test_case(anchors, term):
	hits = {}
	test_case = []
	for item in anchors + [term]:
		hits[item] = get_hits(item)
	for anchor in anchors:
		test_case.append(str(normalized_index_distance(hits[term], hits[anchor], get_hits(term + "+" + anchor))))
	return test_case
	
# CROSS-VALIDATION
# CLUSTERING

#EXPERIMENT SETUP
anchors = ["red", "blue", "green", "orange", "google", "lisp", "domain", "little"]
train_positive = ["purple", "brown", "yellow", "pink"]
train_negative = ["metal", "cold", "virus"]

tests = ["crimson", "rose", "tangerine", "grey", "pastel", "design", "colors", "white", "contrast", "beige", "lilac"]

#create_test_set(anchors, tests)
#create_training_set(anchors, train_positive, train_negative)

clss = build_classifier()
for term in tests:
	predict_proba = predict_class(clss, create_test_case(anchors, term))
	rclass = "colors"
	print "semantic_relation("+term+","+rclass+")["+str(float(predict_proba))+"]"	