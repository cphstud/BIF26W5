#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 11:15:51 2026

@author: thor
"""

#!/usr/bin/env python3
import requests as rq
import pandas as pd
import numpy as np


# research goal
# som boligsælger vil jeg gerne kunne indtaste min bolig i en applikation
# som giver mig et bud på en pris
# således at jeg kan beslutte om jeg vil gå igang med et salg

pd.options.display.float_format = '{:,.0f}'.format

###2) data retrieval
dfbolig=pd.read_csv("data/bolig.csv")

###3.1) data cleaning
# pris - numerisk
dfbolig['prisnum']=pd.to_numeric(dfbolig['pris'].str.replace("[. a-z]","",regex=True))

# ejerudg - numerisk
#test=dfboligsub.loc[1:4,'ejerudg']

## kvm - numerisk
# fix df-err vha filtering/subsetting

test=dfboligsub.iloc[4100]
dfboligsub=dfbolig.query('~type.str.startswith("Hel")')
dfboligsub=dfboligsub.query('~type.str.startswith("Friti")')
dfboligsub=dfboligsub.query('~kvm.str.startswith("- ")')

dfboligsub['kvmnum']=pd.to_numeric(dfboligsub['kvm'].str.replace(" m²","",regex=True))

## Energi - kateogori


###3.2) Feature engineering
# alder ud fra årstal
# lav alderskateogori


###4) data exploration
###4.1) simple exploration - numeric

###4.1) simple exploration - numeric

## what are outliers?
# pris

# ejerudgift


###4.1) simple exploration - cateogorial
# energimærke

###4.2) combined - numeric + numeric


###4.2) combined - categorial + numeric
# gennemsnitspris pr emærke







