
import pandas as pd
import numpy as np
import requests as rq
from io import StringIO

pd.options.display.float_format = '{:,.0f}'.format

### 2) data retrieval
dfbolig = pd.read_csv("boligcl4.csv")

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
# ) merge zip-mun sammen med dfbolig
# finde join-kolonne og sikre samme "navn"
resdf.rename(columns={'navn':'postnr'},inplace=True)
resdf2=resdf.drop(columns=['kommunekode','kommuner','href','stormodtageradresser', 'bbox', 'visueltcenter','ændret', 'geo_ændret', 'geo_version', 'dagi_id'])
resdf2=resdf2.drop_duplicates()
dfbolig.rename(columns={'zipcode':'nr'}, inplace=True)
resdf2['nr']=resdf2['nr'].apply(int)


dfboligzip=pd.merge(dfbolig,resdf2,how="left",on="nr")




