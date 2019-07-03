# sklearn packages
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import model_selection, linear_model, metrics

# pandas & numpy
import pandas as pd
import numpy as np
import datetime
import statistics

# load up the sheet of data
train = pd.read_csv("/Users/ndrezn/OneDrive - McGill University/Github/riddles-project/workset/df_organized_dates.csv")

# remove rows missing content and location
train = train[pd.notnull(train.CONTENT)]
train = train[pd.notnull(train.DATE)]
# reset dataframe index
train = train.reset_index()
train = train.loc[:,'ID':'CONTENT']

train['DATE'] = pd.to_datetime(train['DATE'])

def check_date(date):
	if date.year < 1878:
		return 0
	else:
		return 1

def manipulate_meta():
	dates = [check_date(date) for date in train['DATE']]
	train['DATE'] = dates

	locations = train['LOCATION'].tolist()

	# use ints to represent location data
	train.loc[train.LOCATION == "London England", 'LOCATION'] = 0
	train.loc[train.LOCATION == "Melbourne Australia", 'LOCATION'] = 1
	train.loc[train.LOCATION == "Cape Town South Africa", 'LOCATION'] = 1
	train.loc[train.LOCATION == "Phoenix AZ Arizona United States", 'LOCATION'] = 1
	train.loc[train.LOCATION == "Montreal Canada", 'LOCATION'] = 1

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

# Build basic sets
X = final_df.iloc[:, 8:].values    # corresponds to where feature columns begin
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

scores=model_selection.cross_val_score(linear_model.LogisticRegression(penalty='l1', C=1), X, Y, scoring='f1_weighted', cv=10)
print("Mean: " + str(scores.mean()))
print("Stdev: " + str(statistics.stdev(scores)))

print()

# Compute most informative features for binary case

clf = linear_model.LogisticRegression(penalty='l1', C=0.1)
clf.fit(X_train, y_train)
    
feature_names = final_df.columns[5:].values     
class_labels = final_df['DATE'].unique()

top20 = np.argsort(np.exp(clf.coef_))[0][-10:]
print("Top 10 features associated with second class (late riddles)\n")
for el in zip(feature_names[top20], np.exp(clf.coef_)[0][top20]):
    print(el)
print()
print("Top 10 features associated with first class (early riddles)\n")
bottom20 = np.argsort(np.exp(clf.coef_))[0][:10]
for el in zip(feature_names[bottom20], np.exp(clf.coef_)[0][bottom20]):
    print(el)


