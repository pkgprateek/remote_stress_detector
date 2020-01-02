import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("~/Downloads/HeartRate.csv")
df = df.drop('Obs',axis=1)
med = df['HeartRate'].median()
df['Stressed'] = np.where(df['HeartRate']>=med, 1, 0)
print(df.head())
X = df.drop('Stressed',axis=1)
Y = df['Stressed']
model = LogisticRegression()
model.fit(X,Y)
print(model.coef_)
print(model.intercept_)