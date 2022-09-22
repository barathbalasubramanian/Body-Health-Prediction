
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

dataset = pd.read_csv('dataset/bmi_data.csv')

print(dataset.shape)
print(dataset.isnull().sum())

dataset.dropna(inplace = True)
print(dataset.shape)
print(dataset.isnull().sum())
print(dataset['Sex'].unique())
dataset['Sex'].replace({'Male':1,'Female':0},inplace=True)
print(dataset['Sex'].unique())

for i in dataset['BMI'] :
    if i > 25 :
        dataset.replace({i:dataset['BMI'].mean()},inplace=True)
max(dataset['BMI'])

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

print(dataset.columns)

X = dataset.loc[0:24950,['Sex', 'Age', 'Height', 'Weight']]
Y = dataset.loc[0:24950,['BMI']]

from audioop import minmax
from sklearn.preprocessing import MinMaxScaler
MinMax = MinMaxScaler(feature_range=(0, 1)).fit_transform(X,Y)

from sklearn.preprocessing import StandardScaler
standard = StandardScaler()
standard_data = standard.fit_transform(MinMax)

from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree = 30,interaction_only=True,include_bias=False)
data_poly = poly.fit_transform(MinMax)

from sklearn.preprocessing import RobustScaler
robust = RobustScaler().fit_transform(data_poly)

X_train, X_test, Y_train, Y_test = train_test_split(standard_data, Y, random_state=0, train_size = .80)


Random = RandomForestRegressor(n_jobs=-1)
Random.fit(X_train,Y_train)
pred_rand = Random.predict(X_test)

print(r2_score(Y_test,pred_rand))

