import os
os.environ['LOKY_MAX_CPU_COUNT'] = '8'

import pandas
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler, QuantileTransformer
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
import sklearn.metrics as metrics
from sklearn.linear_model import LinearRegression

rawdata = pandas.read_csv('car_price_prediction_with_missing.csv')

print(rawdata.head())

## check nulls by column
print(rawdata.isnull().sum())

## every column has the same number of nulls, lets check if they are the same rows.
print(rawdata.isnull().all(axis=1).sum())

## the rows are fully null and are safe to drop
rawdata.dropna(how='all',inplace= True)

## column data types
print(rawdata.dtypes)

## drop id column
rawdata.drop(columns=['Car ID'])

## get dummies

cleaneddata = pandas.get_dummies(data=rawdata,columns= ['Brand','Fuel Type','Transmission','Condition','Model'])

print(cleaneddata.head())

## Build Features
features = cleaneddata.drop(columns=['Price'])
target = cleaneddata.Price

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.33, random_state=42)

## Linear Regression
lr = LinearRegression()
lr = lr.fit(X_train, y_train)

lrpred = lr.predict(X_test)

print(metrics.mean_absolute_error(y_test,lrpred))
print(metrics.root_mean_squared_error(y_test,lrpred))
print(metrics.r2_score(y_test,lrpred))

# KNN
knn = KNeighborsRegressor(n_neighbors=30)
knn = knn.fit(X_train, y_train)

knnpred = knn.predict(X_test)

print(metrics.mean_absolute_error(y_test,knnpred))
print(metrics.root_mean_squared_error(y_test,knnpred))
print(metrics.r2_score(y_test,knnpred))


# Xgboost
xgb = XGBRegressor(n_estimators = 600)
xgb = xgb.fit(X_train, y_train)

xgbpred = xgb.predict(X_test)

print(metrics.mean_absolute_error(y_test,xgbpred))
print(metrics.root_mean_squared_error(y_test,xgbpred))
print(metrics.r2_score(y_test,xgbpred))
