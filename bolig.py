#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 14:39:12 2026

@author: thor
"""

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
dfbolig.shape

###3) data cleaning
# pris
dfbolig['prisnum']=pd.to_numeric(dfbolig['pris'].str.replace("[\. a-z]","",regex=True))
## kvm
# fix df-err vha filtering

dfboligsub=dfbolig.query('~type.str.startswith("Hel")')
dfboligsub=dfboligsub.query('~type.str.startswith("Friti")')
dfboligsub=dfboligsub.query('~kvm.str.startswith("- ")')

dfboligsub['kvmnum']=pd.to_numeric(dfboligsub['kvm'].str.replace(" m²","",regex=True))

dfboligsub['energiCat']=dfboligsub['energi'].str.replace("[^ABCDEF]","",regex=True)

tet=dfboligsub.iloc[4180]
###4) data exploration
###4.1) simple exploration
dfboligsub['prisnum'].plot.hist(bins=50)
dfboligsub['prisnum'].describe()
dfboligsub['prisnum'].median()

dfboligsub['kvmnum'].plot.hist(bins=50)
dfboligsub['kvmnum'].plot.box()
dfexp=dfboligsub.query('kvmnum > 600')
## what are outliers?
dfexp=dfbolig.query('prisnum > 20000000')

###4.2) combined
dfboligsub.plot.scatter('prisnum','kvmnum' )

