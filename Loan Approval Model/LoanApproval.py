import pandas
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, QuantileTransformer
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix



raw_data = pandas.read_csv('loanapproval.csv')

print(raw_data.head())

raw_data.drop(columns=['applicant_id','gender','age'],inplace=True)

print(raw_data.isna().sum())

corrmatrix = raw_data.corr(numeric_only= True)
print(corrmatrix)

corrmatrix.to_csv('correlation.csv')

cleaneddata = pandas.get_dummies(data=raw_data,columns= ['marital_status','employment_status'])


features = cleaneddata.drop(columns=['loan_approved'])
target = cleaneddata.loan_approved

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.33, random_state=42)

# Logistic Regression
lr = LogisticRegression(max_iter=3000)
lr = lr.fit(X_train, y_train)

lrpred = lr.predict(X_test)

accuracy = accuracy_score(y_test, lrpred)
precision = precision_score(y_test, lrpred,average='weighted')
recall = recall_score(y_test, lrpred,average='weighted')
f1 = f1_score(y_test, lrpred,average='weighted')
cfmatrix = confusion_matrix(y_test, lrpred)

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1-score: {f1}")
print(cfmatrix)


# Random Forest
rdforest = RandomForestClassifier(n_estimators=200)
rdforest = rdforest.fit(X_train, y_train)

rdforestpred = rdforest.predict(X_test)

accuracy = accuracy_score(y_test, rdforestpred)
precision = precision_score(y_test, rdforestpred,average='weighted')
recall = recall_score(y_test, rdforestpred,average='weighted')
f1 = f1_score(y_test, rdforestpred,average='weighted')
cfmatrix = confusion_matrix(y_test, rdforestpred)

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1-score: {f1}")
print(cfmatrix)

# KNN
knn = KNeighborsClassifier(n_neighbors=10)
knn = knn.fit(X_train, y_train)

knnpred = knn.predict(X_test)

accuracy = accuracy_score(y_test, knnpred)
precision = precision_score(y_test, knnpred,average='weighted')
recall = recall_score(y_test, knnpred,average='weighted')
f1 = f1_score(y_test, knnpred,average='weighted')
cfmatrix = confusion_matrix(y_test, knnpred)

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1-score: {f1}")
print(cfmatrix)


# Xgboost
xgb = XGBClassifier(n_estimators=100)
xgb = xgb.fit(X_train, y_train)

xgbpred = xgb.predict(X_test)

accuracy = accuracy_score(y_test, xgbpred)
precision = precision_score(y_test, xgbpred,average='weighted')
recall = recall_score(y_test, xgbpred,average='weighted')
f1 = f1_score(y_test, xgbpred,average='weighted')
cfmatrix = confusion_matrix(y_test, xgbpred)

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1-score: {f1}")
print(cfmatrix)

