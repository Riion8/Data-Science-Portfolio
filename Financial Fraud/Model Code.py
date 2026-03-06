from pyexpat import features
import pandas
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler, QuantileTransformer
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix



raw_data = pandas.read_csv('synthetic_fraud_dataset.csv')

print(raw_data.head())

raw_data.drop(columns=['transaction_id','user_id'],inplace=True)

print(raw_data.isna().sum())

#transaction_type,merchant_category,country
# print(raw_data.transaction_type.unique())
# print(raw_data.merchant_category.unique())
# print(raw_data.country.unique())

transaction_type_map = {
    'ATM': 1,
    'QR':2,
    'Online':3,
    'POS':4
    }

merchant_category_map = {
    'Travel':1,
    'Food':2,
    'Clothing':3,
    'Grocery':4,
    'Electronics':5
    }

country_map = {
    'TR':1,
    'US':2,
    'FR':3,
    'DE':4,
    'UK':5,
    'NG':6
    }

raw_data['transaction_type'].replace(transaction_type_map,inplace=True)
raw_data['merchant_category'].replace(merchant_category_map,inplace=True)
raw_data['country'].replace(country_map,inplace=True)





# ['ATM' 'QR' 'Online' 'POS']
# ['Travel' 'Food' 'Clothing' 'Grocery' 'Electronics']
# ['TR' 'US' 'FR' 'DE' 'UK' 'NG']

#raw_data.corr().to_csv('feature_corr.csv')

# drop highly correlated columns
raw_data.drop(columns=['device_risk_score','ip_risk_score'],inplace=True)

features = raw_data.drop(columns=['is_fraud'])
target = raw_data.is_fraud

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.33, random_state=42)
#bu



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
