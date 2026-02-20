import requests as rq
import pandas as pd
import json
from pyproj import Transformer
import numpy as np
from sklearn.neighbors import KDTree
from datetime import datetime


pd.options.display.float_format = '{:,.0f}'.format
dfbolig4=pd.read_csv("dfboligzip.csv")
dfboligorig=pd.read_csv("boligclean.csv")
dfboligorig['grundnum'] = dfboligorig['grund'].str.replace(" m²", "", regex=True)
dfboligorig['grundnum'] = pd.to_numeric(dfboligorig['grundnum'].str.replace("[^0-9]", "", regex=True))
dfboligorigsub=dfboligorig[['bolig_id','grundnum']]

dfbolig4.loc[3].vejnavncl
dfbolig4['lookupurl']=dfbolig4['vejnavncl'].apply(lambda x: len(x))
dfbolig4['lookupurl']=dfbolig4.apply(lambda x: x['vejnavncl'])
dfbolig4['lookupurl']="https://api.dataforsyningen.dk/adresser?vejnavn=" + dfbolig4['vejnavncl']+"&husnr="+dfbolig4['streetnr'].apply(str)+"&postnr="+dfbolig4['nr'].apply(str)

dfbolig4sub=dfbolig4[1:10]

logfile=open("mylog.txt","a",encoding="utf-8")
OUTPUT_FILE = "addresses3.jsonl"

def getStuff(row):
    #row=testurl
    res=rq.get(row)
    #print(res.status_code)
    try:
        data=res.json()
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            for element in data:
                json.dump(element, f, ensure_ascii=False)
                f.write("\n")
    except:
        logfile.write(f"{row}\n")
    
    #t
    #nyt=t['adgangsadresse']
    #nyt['kommune']['navn']
testurl=dfbolig4sub.loc[3,'lookupurl']
getStuff(testurl)
    
dfbolig4['lookupurl'].apply(getStuff)
(dfbolig4sub.isna().count())

mylist=list()
mylist.append("kurt")
mylist.append(123123)

addresses = []

with open("addresses3.jsonl", encoding="utf-8") as f:
    for line in f:
        addresses.append(json.loads(line))
        

def newenrich(data):

    try:
        adgang = data["adgangsadresse"]
        

        retval= pd.Series({
            "kommune": adgang["kommune"]["navn"],
            "vej": adgang["vejstykke"]["navn"],
            "husnr": adgang["husnr"],
            "postnr": adgang["postnummer"]["nr"],
            "lat": adgang["adgangspunkt"]["koordinater"][1],
            "lon": adgang["adgangspunkt"]["koordinater"][0],
            "hojde": adgang["adgangspunkt"]["højde"],
            "region": adgang["region"]["navn"],
            "landsdel": adgang["landsdel"]["navn"],
            "afstemningssted_url": adgang["afstemningsområde"]["href"],
            "afstemningssted_by": adgang["afstemningsområde"]["navn"]
        })
        return retval

    except Exception as e:
        logfile.write(str(e) + "\n")

        # VERY IMPORTANT: return same columns when failing1G
        return pd.Series({
            "kommune": None,
            "vej": None,
            "husnr": None,
            "postnr": None,
            "lat": None,
            "lon": None,
            "hojde": None,
            "region": None,
            "landsdel": None,
            "afstemningssted_url": None,
            "afstemningssted_by": None
        })


addr_df2 = pd.DataFrame([newenrich(a) for a in addresses])
addr_df2.drop_duplicates(inplace=True)
dfbolig4.rename(columns={'vejnavncl':'vej'}, inplace=True)
#dfbolig4.rename(columns={'vej':'vejtot'}, inplace=True)
dfbolig4.rename(columns={'streetnr':'husnr'}, inplace=True)
dfbolig4.rename(columns={'postnr_x':'postnrnavn'}, inplace=True)
dfbolig4.rename(columns={'nr':'postnr'}, inplace=True)
dfbolig4.info()
addr_df2.info()
addr_df2['husnr']=addr_df2['husnr'].apply(int)
addr_df2['postnr']=addr_df2['postnr'].apply(int)
#dfbolig4.drop(dfbolig4.columns[4], axis=1, inplace=True)
dfbolig4merge = dfbolig4.merge(addr_df2, on=["vej","husnr","postnr"], how="left")

# now lat long
tf = Transformer.from_crs("EPSG:4326", "EPSG:25832", always_xy=True)
dfbolig4merge["x"], dfbolig4merge["y"] = tf.transform(dfbolig4merge.lon.values, dfbolig4merge.lat.values)

dfbolig4mergesub=dfbolig4merge.dropna()
dfbolig4mergesub["y"] = dfbolig4mergesub["y"].astype("int64")
XY = dfbolig4mergesub[["x","y"]].to_numpy()
tree = KDTree(XY)
radius = 500  # meters (very important hyperparameter)

neighbors = tree.query_radius(XY, r=radius)

local_price = []

prices = dfbolig4mergesub["prisnum"].to_numpy()

for i, inds in enumerate(neighbors):
    inds = inds[inds != i]  # remove itself
    if len(inds) == 0:
        local_price.append(prices.mean())
    else:
        local_price.append(prices[inds].mean())

dfbolig4mergesub["local_price_level"] = local_price
dfbolig4mergesub["local_price_level"]=dfbolig4mergesub["local_price_level"].astype("int64")
dfbolig4mergesub["local_price_level"].describe()

# rejseplanen
#https://www.rejseplanen.dk/api/location.nearbystops?accessId=b9d07397-4f68-4896-97cb-06f812489cbc
#&originCoordLat=56.210099&originCoordLong=10.03619033


#https://www.rejseplanen.dk/api/location.nearbystops?accessId=b9d07397-4f68-4896-97cb-06f812489cbc
#&format=json&originCoordLat=55.65116712&originCoordLong=8.14560786


#https://www.rejseplanen.dk/api/location.nearbystops?accessId=b9d07397-4f68-4896-97cb-06f812489cbc
#&originCoordLat=56.210099&originCoordLong=10.03619033  


#https://www.rejseplanen.dk/api/trip?accessId=b9d07397-4f68-4896-97cb-06f812489cbc
#&format=json&originCoordLat=55.9346752&originCoordLong=9.2968517
#&destCoordLat=55.6737846&destCoordLong=12.5605089

dfbolig4mergesub['landsdel'].value_counts()
dfbolig4mergesub['region'].value_counts()
dfbolig4mergesub['kommunenavn'].value_counts()

dfbolig4mergesub['region'].unique()

region_to_capital = {
    "Region Midtjylland": "10.2021091,56.1502982",
    "Region Hovedstaden": "12.5630892,55.6727611",
    "Region Syddanmark": "9.4786398,55.4907965",
    "Region Sjælland": "12.5630892,55.6727611",
    "Region Nordjylland":"9.914491, 57.0431251"
}

dfbolig4mergesub['regionsby']=dfbolig4mergesub['region'].map(region_to_capital)
dfbolig4mergesub['regionsbylat']=dfbolig4mergesub['regionsby'].apply(lambda x: x.split(",")[1])
dfbolig4mergesub['regionsbylong']=dfbolig4mergesub['regionsby'].apply(lambda x: x.split(",")[0])
dfbolig4mergesub['regionsbylat']=dfbolig4mergesub['regionsbylat'].apply(str)
dfbolig4mergesub['regionsbylong']=dfbolig4mergesub['regionsbylong'].apply(str)
dfbolig4mergesub['lat']=dfbolig4mergesub['lat'].apply(str)
dfbolig4mergesub['lon']=dfbolig4mergesub['lon'].apply(str)

# lookup traveltime to regionsby
apikey="b9d07397-4f68-4896-97cb-06f812489cbc"
# subset for testing
boligsub=dfbolig4mergesub.sample(n=5).reset_index()
baseurl=f"https://www.rejseplanen.dk/api/location.nearbystops?accessId={apikey}"
baseurltrip=f"https://www.rejseplanen.dk/api/trip?accessId={apikey}"
dfbolig4mergesub['travelurl']=baseurltrip+"&format=json&originCoordLat="+dfbolig4mergesub['lat']+\
    "&originCoordLong="+dfbolig4mergesub['lon']+\
        "&destCoordLat="+dfbolig4mergesub['regionsbylat']+\
            "&destCoordLong="+dfbolig4mergesub['regionsbylong']+\
                "&date=2026-03-03&time=08:00"
boligsub.info()
testurl=boligsub.travelurl[0]
testurl

# now loop and save to jsonL

logfile=open("mylogrejseplan.txt","a",encoding="utf-8")
OUTPUT_FILE = "rejseplantest.jsonl"

def getRejse(row):
    minutes=None
    #row=testurl
    res=rq.get(row)

    #print(res.status_code)
    try:
        data=res.json()
        trips = data.get("Trip", [])
        mtrip=trips[0]
        t1=mtrip['Origin']['time']
        t2=mtrip['Destination']['time']
        fmt = '%H:%M:%S'
        time1 = datetime.strptime(t1, fmt)
        time2 = datetime.strptime(t2, fmt)

        diff = time2 - time1
        minutes = diff.total_seconds() / 60
    except:
        logfile.write(f"{row}\n")
    return(minutes)
    #t
    #nyt=t['adgangsadresse']
    #nyt['kommune']['navn']
testurl=boligsub.loc[3,'travelurl']
boligsub.iloc[3,]
testurl                


getRejse(testurl)
    
dfbolig4mergesub['traveltime']=dfbolig4mergesub['travelurl'].apply(getRejse)
dfbolig4mergesub.plot.scatter(x='traveltime', y='prisnum')


travels = []

with open("rejseplan.jsonl", encoding="utf-8") as f:
    for line in f:
        travels.append(json.loads(line))
        

test=travels[31]
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

dfbolig4mergesub2=pd.merge(dfbolig4mergesub,dfboligorigsub, how="left", on="bolig_id")
dfbolig4mergesub2['liggetidnum']=pd.to_numeric(dfbolig4mergesub2['liggetid'].str.replace("[^0-9]","",regex=True))
dfbolig4mergesub2['liggetidnum'].fillna(0)
dfbolig4mergesub2['grundnum'].fillna(0)
dfbolig4mergesub2['traveltime'].fillna(dfbolig4mergesub2['traveltime'].mean(),inplace=True)

dfbolig4mergesub2=dfbolig4mergesub2.reset_index()
X = dfbolig4mergesub2[["hojde","kvmnum","aldernum","liggetidnum","traveltime","grundnum"]]
y = dfbolig4mergesub2["prisnum"]

X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
X.info()
X.isna().sum()
s



