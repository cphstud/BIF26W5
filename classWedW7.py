import pandas as pd
import numpy as np
import requests as rq
from io import StringIO

pd.options.display.float_format = '{:,.0f}'.format

### 2) data retrieval
dfbolig = pd.read_csv("data/bolig.csv")
dfbolig = pd.read_csv("boligcl4.csv")


### 3 DATA PREPARATION
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

# grund – numerisk
dfboligsub['grundnum'] = dfboligsub['grund'].str.replace(" m²", "", regex=True)
dfboligsub['grundnum'] = pd.to_numeric(dfboligsub['grundnum'].str.replace("[^0-9]", "", regex=True))

# værelser – numerisk(?)
dfboligsub['vaercat'] = pd.to_numeric(dfboligsub['vaer'].str.replace("[^0-9]", "", regex=True))

### Energi – kategori
testrækker = dfboligsub.loc[1:5, 'energi']
testrækker2 = dfboligsub['energi'].value_counts()
dfboligsub['energicat'] = dfboligsub['energi'].str.replace("Energimærke ", "")
testrækker2 = dfboligsub['energicat'].value_counts()
dfboligsub['energicat'] = dfboligsub['energicat'].str.replace("Intet energimærke", "I")
dfboligsub['energicat'] = dfboligsub['energicat'].str.replace("A[0-9]+", "A", regex=True)

### additional clean on vejnavn
dfboligsub2['vejnavncl']=dfboligsub2['vejname'].str.replace('-\d+\w*','', regex=True)
dfboligsub2['vejnavncl']=dfboligsub2['vejnavncl'].str.title()
dfboligsub2['vejnavncl']=dfboligsub2['vejnavncl'].str.replace("\d","")
dfboligsub2['vejnavncl']=dfboligsub2['vejnavncl'].str.replace("ae","æ")
dfboligsub2['vejnavncl']=dfboligsub2['vejnavncl'].str.replace("aa","å")
dfboligsub2['vejnavncl']=dfboligsub2['vejnavncl'].str.replace("oe","ø")
dfboligsub2['vejnavncl']=dfboligsub2['vejnavncl'].str.replace("Aa","Å")
dfboligsub2['vejnavncl']=dfboligsub2['vejnavncl'].str.replace("Ae","Æ")
dfboligsub2['vejnavncl']=dfboligsub2['vejnavncl'].str.replace("Oe","Ø")
dfboligsub2['vejnavncl']=dfboligsub2['vejnavncl'].str.replace("-"," ")


# fjern boliger uden energimærke
dfboligsub = dfboligsub.query('~energicat.str.contains("I")')

### 3.2) data transformation

# alder ud fra årstal
#dfboligsub['alder'] = dfboligsub['opført']
dfboligsub['aldernum'] = 2025 - pd.to_numeric(dfboligsub['alder'].str.replace("Opført ", "", regex=True))

### 3.3) combining data
dfboligsub2=dfboligsub.drop(columns=['pris', 'energi', 'type', 'kvm', 'ejerudg', 'grund', 'vaer','alder','zipmunic','zipplace','kvm2'])
### 3.3.1) Merging from external source - dataforsyningen

# z) adresselookup

# a) først json
url="https://api.dataforsyningen.dk/postnumre"
res=rq.get(url)
res.status_code
resdf=pd.DataFrame(res.json())

# undersøg 1 element
testr=resdf.loc[567,'kommuner']
testr2=testr[0]['navn']
testr2.values()
testr2['navn']
zipnametest=testr[0]['navn']

def getNavn(row):
    return(row[0]['navn'])
# loop igennem hele dataframen
resdf['kommunenavn']=resdf['kommuner'].apply(lambda x: x[0]['navn'] )
resdf['kommunekode']=resdf['kommuner'].apply(lambda x: x[0]['kode'] )
resdf['kommunenavn']=resdf['kommuner'].apply(getNavn)

# ) merge zip-mun sammen med dfbolig
# finde join-kolonne og sikre samme "navn"
resdf.rename(columns={'navn':'postnr'},inplace=True)
resdf2=resdf.drop(columns=['kommunekode','kommuner','href','stormodtageradresser', 'bbox', 'visueltcenter','ændret', 'geo_ændret', 'geo_version', 'dagi_id'])
resdf2=resdf2.drop_duplicates()
dfbolig.rename(columns={'mzip':'nr'}, inplace=True)
resdf2['nr']=resdf2['nr'].apply(int)


dfboligzip=pd.merge(dfboligsub2,resdf2,how="left",on="nr")

dfboligzip.to_csv("dfboligzip.csv", index=False)
# 
# ) merge mun-population sammen med dfbolig
# get all tables
from denstatbank import StatBankClient
sbc=StatBankClient()
tb=sbc.tableinfo("folk1a", variables_df=True)


params = {
    'table': 'folk1a',
    'format': 'CSV',
    'delimiter': 'Semicolon',
    'variables': [
        {'code': 'OMRÅDE', 'values': ['*']},
        {'code': 'ALDER', 'values': ['IALT']},
        {'code': 'CIVILSTAND', 'values': ['TOT']},
        {'code': 'Tid', 'values': ['2025K4']}
    ]
}
r = rq.post('https://api.statbank.dk/v1' + '/data', json=params)
r.status_code
print(r.text[:200])
df = pd.read_csv(StringIO(r.text), sep=';')
df.drop(columns=['ALDER', 'CIVILSTAND', 'TID'],inplace=True)
# merge ind i dfbolig
df.rename(columns={'OMRÅDE':'kommunenavn'}, inplace=True)
dfboligzippop=pd.merge(dfboligzip,df,how="left",on="kommunenavn" )
    



### 4) data exploration

#### 4.1) simple exploration – numeric
dfboligsub['prisnum'].plot.hist(bins=50)
dfboligsub['ejerudgnum'].plot.hist(bins=90)
dfboligsub['kvmnum'].plot.hist(bins=50)
dfboligsub['grundnum'].plot.box()
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
c=dfboligzippop['kvmnum'].corr(dfboligzippop['ejerudgnum'])
pd_correlation = df["inc_cnt_bfr"].corr(df["inc_cnt_bfr"])








