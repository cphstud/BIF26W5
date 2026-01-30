import requests as rq
import pandas as pd
import numpy as np



# 

### 1) research goal
# som sælger af min bil vil jeg gerne kunne indtaste min bils data i en applikation
# som giver mig et bud på en pris
# således at jeg kan beslutte om jeg vil gå igang med et salg

pd.options.display.float_format = '{:,.0f}'.format
dfcar.isna().sum()

###2) data retrieval
dfcar=pd.read_csv("data/bilbasen.csv")

###3.1) data cleaning
# do an info and report number of numeric and categorial variables

### 3.1.1)
## check for NaN's 
# create a dataframe with those cars
# decide on what you would fill in if you keep them




###3.2) Feature engineering
##3.2.1) numeriske
# alder ud fra årstal

# slagvolumen ud fra maketype-kolonnen

##3.2.2) kategoriske

# antal døre ud fra maketype-kolonnen

# benzin-økonomi ud fra slagvolumen (4 kategorier)

# alderskategori ud fra alder (5 kategorier)


###4) data exploration 
###4.1) simple exploration - numeric
### make sure to locate outliers and decide on thresholds


###4.1) simple exploration - cateogorial


###4.2) combined - numeric + numeric


###4.2) combined - categorial + numeric
# gennemsnitspris pr mærke
# gennemsnitspris pr region



