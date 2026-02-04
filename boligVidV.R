import pandas as pd
import numpy as np

pd.options.display.float_format = '{:,.0f}'.format

### 2) data retrieval
dfbolig = pd.read_csv("data/bolig.csv")

### 3.1) data cleaning

# pris – numerisk
dfbolig['prisnum'] = pd.to_numeric(dfbolig['pris'].str.replace("[. a-z]", "", regex=True))

# subset data
dfboligsub = dfbolig.query('~type.str.startswith("Hel")')
dfboligsub = dfboligsub.query('~type.str.startswith("Fritid")')
dfboligsub = dfboligsub.query('~kvm.str.startswith("-")')

# ejerudg – numerisk
dfboligsub['ejerudgnum'] = pd.to_numeric(dfboligsub['ejerudg'].str.replace("[. a-zA-Z/]", "", regex=True))

# kvm – numerisk
dfboligsub['kvmnum'] = pd.to_numeric(dfboligsub['kvm'].str.replace(" m²", "", regex=True))

### Energi – kategori
testrækker = dfboligsub.loc[1:5, 'energi']
testrækker2 = dfboligsub['energi'].value_counts()
dfboligsub['energicat'] = dfboligsub['energi'].str.replace("Energimærke ", "")
testrækker2 = dfboligsub['energicat'].value_counts()
dfboligsub['energicat'] = dfboligsub['energicat'].str.replace("Intet energimærke", "I")
dfboligsub['energicat'] = dfboligsub['energicat'].str.replace("A[0-9]+", "A", regex=True)

# fjern boliger uden energimærke
dfboligsub = dfboligsub.query('~energicat.str.contains("I")')

### 3.2) Feature engineering

# alder ud fra årstal
#dfboligsub['alder'] = dfboligsub['opført']
dfboligsub['aldernum'] = 2024 - pd.to_numeric(dfboligsub['alder'].str.replace("Opført ", "", regex=True))

### 4) data exploration

#### 4.1) simple exploration – numeric
dfboligsub['prisnum'].plot.hist(bins=50)
dfboligsub['ejerudgnum'].plot.hist(bins=90)
dfboligsub['kvmnum'].plot.hist(bins=50)
dfboligsub['aldernum'].plot.hist(bins=50)
dfboligsub['aldernum'].plot.box()

#### 4.1) simple exploration – categorical
testrækker2.plot.bar()


#### 4.2) combined – numeric + numeric
dfboligsub.plot.scatter(x='kvmnum', y='prisnum')
dfboligsub.plot.scatter(x='ejerudgnum', y='prisnum')
dfboligsub.plot.scatter(x='aldernum', y='prisnum')

#### 4.2) combined – categorical + numeric
statenergi = (dfboligsub.groupby('energicat')['prisnum'].mean().astype(int).reset_index())

statenergi.plot.bar(x='energicat', y='prisnum')

