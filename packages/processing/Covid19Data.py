# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 07:59:45 2020

@author: raja
"""


import pandas as pd
import numpy as np

class Covid19Data:
    dataUrl = []
    fnames = []
    countryNames = []
    confDF = pd.DataFrame()
    dtsDF = pd.DataFrame()
    recoveredDF = pd.DataFrame()
    
    def __init__(self):
        
        self.dataUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
        self.fnames = ("time_series_covid19_confirmed_global.csv",
                  "time_series_covid19_deaths_global.csv",
                  "time_series_covid19_recovered_global.csv")
                
    def updateCountryNames(self):
         
        self.countryNames = self.confDF["Country/Region"].unique()
        
    def getCountryNameIndex(self, countryName="Canada"):
         
        return np.argmax(self.countryNames == "Canada")
        
         
    def loadData(self):
        
        self.confDF = pd.read_csv(self.dataUrl + self.fnames[0])
        self.dtsDF = pd.read_csv(self.dataUrl + self.fnames[1])
        self.recoveredDF = pd.read_csv(self.dataUrl + self.fnames[2])
        
        self.updateCountryNames()
        
           
    
    def aggregateAllDataByCountryName(self,countryName="Canada"):
        outputDF = pd.DataFrame(columns=["confirmed","recovered","deaths"])
        outputDF["confirmed"] = pd.DataFrame(self.confDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat","Long"]).transpose()[countryName]
        outputDF["deaths"] = pd.DataFrame(self.dtsDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat","Long"]).transpose()[countryName]
        outputDF["recovered"] = pd.DataFrame(self.recoveredDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat","Long"]).transpose()[countryName]
        
        #outputDF = pd.DataFrame(inputDFConf.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"]).transpose()
        outputDF.index = pd.to_datetime(outputDF.index)
        
        return outputDF
    
    def getCumulativeDataSummary(self,countryNameOptions="Canada"):
        
        outputStr = """\\begin{matrix}"""
        outputStr += """\\scriptsize \\bf {:%B, %d, %Y} && \\large \\bf Confirmed && \\large \\bf Recovered && \\large \\bf Deaths \\cr[5pt]""".format(pd.to_datetime(self.confDF.columns[-1]))
        outputStr += """\\normalsize \\bf Global && \\normalsize \\bf {:,} && \\normalsize \\bf {:,} && \\normalsize \\bf {:,} \\cr[2pt]""" \
                    .format(self.confDF.iloc[:,-1].sum(),self.recoveredDF.iloc[:,-1].sum(),self.dtsDF.iloc[:,-1].sum())
        for cname in countryNameOptions:
            countryCumTotals = self.aggregateAllDataByCountryName(cname).iloc[-1,:]
            outputStr += """\\normalsize  {} && \\normalsize {:,} && \\normalsize {:,} && \\normalsize {:,} \\cr[2pt]""" \
                        .format(cname, countryCumTotals[0], countryCumTotals[1], countryCumTotals[2])
        outputStr += """\\end{matrix}"""
                        
                        
        return outputStr
    
    def getDailyCountsByCountry(self,option="confirmed", ncases=0):
        
        if(option=="confirmed"):
            outputDF = pd.DataFrame(self.confDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="recovered"):
            outputDF = pd.DataFrame(self.recoveredDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="deaths"):
            outputDF = pd.DataFrame(self.dtsDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        
        # drop rows below ncases
        outputDF = outputDF.drop(outputDF.index[outputDF.iloc[:,-1] < ncases])
               
        outputDF = outputDF.sort_values(by=outputDF.columns[-1], ascending=False)
        
        return outputDF
    
    def getDailyChangeRateByCountry(self,option="confirmed", ncases=0):
        
        if(option=="confirmed"):
            outputDF = pd.DataFrame(self.confDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="recovered"):
            outputDF = pd.DataFrame(self.recoveredDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="deaths"):
            outputDF = pd.DataFrame(self.dtsDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        
        # drop rows below ncases
        outputDF = outputDF.drop(outputDF.index[outputDF.iloc[:,-1] < ncases])
       
       
        for icol in range(len(outputDF.columns)-1,0,-1):
            outputDF.iloc[:,icol] = ((outputDF.iloc[:,icol] - outputDF.iloc[:,icol-1])/outputDF.iloc[:,icol-1])*100
        
        
        outputDF = outputDF.sort_values(by=outputDF.columns[-1], ascending=False)
        
        return outputDF
    
    

# myData = Covid19Data()
# myData.loadData()

# print(myData.getDailyCountsByCountry("confirmed"))
# print(myData.getDailyChangeRateByCountry("confirmed"))