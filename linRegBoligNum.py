import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt


dfbolig9=pd.read_csv("out.csv")

# clean columns
dfbolig9=dfbolig9.drop(columns=['liggetid','Unnamed: 0.2', 'Unnamed: 0.1', 'level_0', 'index', 'Unnamed: 0','vejtot','local_price_level'])

dfbolig9.info()


# Tjek NA
dfbolig9.isna().sum()

# filter only numeric
dfnum = dfbolig9[["prisnum","hojde","kvmnum","aldernum","liggetidnum","traveltime","grundnum"]]

# tjek outliers
dfnum['kvmnum'].plot.box()
dfnum['kvmnum'].describe()
dfnum['aldernum'].plot.box()
dfnum['aldernum'].describe()
dfnum['hojde'].plot.box()
dfnum['hojde'].describe()
dfnum['liggetidnum'].plot.box()
dfnum['liggetidnum'].describe()
dfnum['traveltime'].plot.box()
dfnum['traveltime'].describe()
dfnum['grundnum'].plot.box()
dfnum['grundnum'].describe()
dfnum['prisnum'].plot.box()
dfnum['prisnum'].describe()


#correlations?
cm=dfnum.corr()
plt.figure(figsize=(8,6))
sn.heatmap(cm, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)

# remove outliers
dfbolig9cl=dfnum.query('prisnum < 20000000 and grundnum > 1 and grundnum < 5000 and kvmnum < 500 and aldernum < 200 and liggetidnum < 365')

# remidy skewness
dfbolig9cl['prisnumlog']=np.log(dfbolig9cl["prisnum"])

#import ML-libraries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
lin = LinearRegression()

# prepare split
features = [
    "hojde",
    "kvmnum",
    "aldernum",
    "liggetidnum",
    "traveltime",
    "grundnum"]
X = dfbolig9cl[features].copy()
y = dfbolig9cl["prisnumlog"].copy()

#split
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.25, random_state=42 )

# fit the model to training data

lin.fit(X_train, y_train)

# predict on test
pred = lin.predict(X_test)

# print the metrics for validation
r2  = r2_score(y_test, pred)
mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))

print("R2:", r2)
print("MAE:", mae)
print("RMSE:", rmse)

# remember that its the log-price. 




