import pandas as pd
import numpy as np
import seaborn as sn


# hente data
dfbolig7=pd.read_csv("data/out.csv")

# filter numeric variables
dfnum=dfbolig7[["prisnum","hojde","kvmnum","aldernum","liggetidnum","traveltime","grundnum"]]

#  tjek na
dfnum.isna().sum()

# tjek outliers
dfnum['prisnum'].plot.box()
dfnumcl['prisnum'].plot.hist()
dfnum['prisnum'].describe()
dfnum['hojde'].plot.box()
dfnum['hojde'].describe()
dfnum['kvmnum'].plot.box()
dfnum['kvmnum'].describe()
dfnum['aldernum'].plot.box()
dfnum['aldernum'].describe()
dfnum['grundnum'].plot.box()
dfnum['grundnum'].describe()
dfnum['liggetidnum'].plot.box()
dfnum['liggetidnum'].describe()


dfnumcl=dfnum.query('prisnum < 12000000 and kvmnum < 400 and aldernum < 200 and grundnum > 0 and grundnum < 3000 and liggetidnum < 500')
dfnumcl['grundnum'].plot.box()

# correlations
cm=dfnumcl.corr()
sn.heatmap(cm, annot=True)


# ML delen
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

scaler=StandardScaler()

# opret X (uafhængige) og y (afhængige)
X=dfnumcl[["hojde","kvmnum","aldernum","liggetidnum","traveltime","grundnum"]]
X=scaler.fit_transform(dfnumcl[["hojde","kvmnum","aldernum","liggetidnum","traveltime","grundnum"]])
y=np.log(dfnumcl[['prisnum']])

# opdel i træning og test
X_train, X_test, y_train, y_test =train_test_split(X, y, test_size=0.2)

# fit data til model
lr=LinearRegression()

model=lr.fit(X_train, y_train)

# predict vha modellen
predpris=lr.predict(X_test)

# nu validér model
from sklearn.metrics import r2_score

r2pris=r2_score(y_test,predpris)
print(r2pris)










