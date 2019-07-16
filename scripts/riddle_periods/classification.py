# functionality:
# classifier for the Gale riddle set. 
# classifies using logistic regression based on publication and date. Adjust test number and 
# k-value for different tests (specifications below.) Based on a classifier by Richard So.

# sklearn packages
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import model_selection, linear_model, metrics

# pandas & numpy
import pandas as pd
import numpy as np
import datetime
import statistics

# 0 to classify between the four most popular publications and all other publications
# 1 to classify between the four most popular publications (does not print distinguishing features)
# 2 to classify as either early or late period
test = 0
# number of folds for cross validation
k = 30

# load up the sheet of data
train = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/gale/cleaned_metadata.csv")

# clean up the dataframe
train = train[pd.notnull(train.CONTENT)]
copy = train.loc[:,'ID':'CONTENT']

train['DATE'] = pd.to_datetime(train['DATE'])
pubs = ['Our Young Folk\'s Weekly Budget', \
		'Boys of England: A Magazine of Sport, Sensation, Fun, and Instruction', \
		'The World of Fashion and Continental Feuilletons', \
		'Kind Words for Boys and Girls']
if test == 0:
	train = train[pd.notnull(train.PUBLICATION)]
elif test == 1:
	train = train.loc[train['PUBLICATION'].isin(pubs)]
elif test == 2:
	train = train[pd.notnull(train.DATE)]

# reset dataframe index
train = train.reset_index()
train = train.loc[:,'ID':'CONTENT']

# simple method to print to the screen the publications/locations and number of riddles from each
def count_trait():
	publication = copy.PUBLICATION.tolist()

	pub = {}

	for publ in publication:
		if publ not in pub.keys():
			pub[publ] = 1
		else:
			pub[publ] += 1

	for key,value in pub.items():
		print(key + ": " + str(value))
	print(len(pub))

# returns either early or late riddle
def check_date(date):
	if date.year < 1878:
		return 0
	else:
		return 1

# returns either popular publication or unpopular publication
def check_pub(pub):
	if pub in pubs:
		return 0
	else:
		return 1

# handles metadata tagging based on test being run
def manipulate_meta():
	if test == 0:
		pub_int = [check_pub(pub) for pub in train['PUBLICATION']]
		train['PUBLICATION'] = pub_int
	if test == 1:
		pub_int = [pubs.index(pub) for pub in train['PUBLICATION']]
		train['PUBLICATION'] = pub_int
	if test == 2:
		dates = [check_date(date) for date in train['DATE']]
		train['DATE'] = dates

manipulate_meta()

# build a document term matrix
vectorizer = CountVectorizer(stop_words='english', min_df=3, encoding='utf8')
dtm = vectorizer.fit_transform(train['CONTENT'])
vocab = vectorizer.get_feature_names()
matrix = dtm.toarray()

DTM = pd.DataFrame(matrix, columns=vocab)

# consolidate metadata with document-term matrix
final_df = pd.concat([train, DTM], axis=1)

# Reset dataframe index
final_df = final_df.reset_index()

# print update
print('Done preparing dataset.')

# build X and Y trainer sets
X = final_df.iloc[:, 8:].values    # corresponds to where feature columns begin
if test == 0 or test == 1:
	Y = final_df.PUBLICATION.values # corresponds to where class values are located
else:
	Y = final_df.DATE.values # corresponds to where class values are located

# Generate train/test sets
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y, test_size=0.3, random_state=0)

# Fit the model, only on training set (no test set)
# Specify regularization penalties
model2 = linear_model.LogisticRegression(penalty='l2', C=1) # Remember l1 is lasso
model2.fit(X_train, y_train)

print('Model fitted.')

# predict class labels for the test set
predicted = model2.predict(X_test)
# generate class probabilities
probs = model2.predict_proba(X_test)

# Now, evaluate model with cross-validation
scores=model_selection.cross_val_score(linear_model.LogisticRegression(penalty='l1', C=1), X, Y, scoring='f1_weighted', cv=k)
print(len(scores))
print("Mean: " + str(scores.mean()))
print("Stdev: " + str(statistics.stdev(scores)))

if test == 1:
	exit()

print()

# Compute most informative features for binary case
clf = linear_model.LogisticRegression(penalty='l1', C=0.1)
clf.fit(X_train, y_train)
    
feature_names = final_df.columns[5:].values     

top20 = np.argsort(np.exp(clf.coef_))[0][-10:]
if test == 2:
	print("Top 10 features associated with late riddles:\n")
else:
	print("Top 10 features associated with obscure journals:\n")
for feature, use in zip(feature_names[top20], np.exp(clf.coef_)[0][top20]):
    print(feature + ": " + str(use))

print()

if test == 2:
	print("Top 10 features associated with early riddles:\n")
else:
	print("Top 10 features associated with popular journals:\n")

bottom20 = np.argsort(np.exp(clf.coef_))[0][:10]
for feature,use in zip(feature_names[bottom20], np.exp(clf.coef_)[0][bottom20]):
    print(feature + ": " + str(use))


