# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 07:59:45 2020

@author: raja
"""


import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Covid19Data:
    dataUrl = []
    fnames = []
    countryNames = []
    confDF = pd.DataFrame()
    dtsDF = pd.DataFrame()
    recoveredDF = pd.DataFrame()
    activeDF = pd.DataFrame()
    
    def __init__(self):
        
        self.dataUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
        self.fnames = ("time_series_covid19_confirmed_global.csv",
                  "time_series_covid19_deaths_global.csv",
                  "time_series_covid19_recovered_global.csv")
                
    def updateCountryNames(self):
         
        self.countryNames = self.confDF["Country/Region"].unique()
        
    def getCountryNameIndex(self, countryName="canada"):
         
        return np.argmax(self.countryNames == "canada")
        
         
    def loadData(self):
        
        self.confDF = pd.read_csv(self.dataUrl + self.fnames[0])
        self.dtsDF = pd.read_csv(self.dataUrl + self.fnames[1])
        self.recoveredDF = pd.read_csv(self.dataUrl + self.fnames[2])
        
        self.confDF["Country/Region"] = self.confDF["Country/Region"].str.lower()
        self.dtsDF["Country/Region"] = self.dtsDF["Country/Region"].str.lower()
        self.recoveredDF["Country/Region"] = self.recoveredDF["Country/Region"].str.lower()
        
        
        self.activeDF = self.confDF.copy()
        self.activeDF.iloc[:,4:] = self.confDF.iloc[:,4:] - self.recoveredDF.iloc[:,4:] - self.dtsDF.iloc[:,4:]
        
        self.updateCountryNames()
        
           
    
    def aggregateAllDataByCountryName(self,countryName="canada"):
        outputDF = pd.DataFrame(columns=["confirmed","recovered","deaths"])
        outputDF["confirmed"] = pd.DataFrame(self.confDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat","Long"]).transpose()[countryName]
        outputDF["deaths"] = pd.DataFrame(self.dtsDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat","Long"]).transpose()[countryName]
        outputDF["recovered"] = pd.DataFrame(self.recoveredDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat","Long"]).transpose()[countryName]
        outputDF["active"] = outputDF["confirmed"] - outputDF["recovered"] - outputDF["deaths"]
        
        #outputDF = pd.DataFrame(inputDFConf.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"]).transpose()
        outputDF.index = pd.to_datetime(outputDF.index)
        
        return outputDF
    
    def getCumulativeDataSummary(self,countryNameOptions="canada"):
        
        outputStr = """\\begin{matrix}"""
        outputStr += """\\scriptsize \\bf {:%B, %d, %Y} && \\large \\bf Confirmed && \\large \\bf Recovered && \\large \\bf Deaths \\cr[5pt]""".format(pd.to_datetime(self.confDF.columns[-1]))
        outputStr += """\\normalsize \\bf Global && \\normalsize \\bf {:,} && \\normalsize \\bf {:,} && \\normalsize \\bf {:,} \\cr[2pt]""" \
                    .format(self.confDF.iloc[:,-1].sum(),self.recoveredDF.iloc[:,-1].sum(),self.dtsDF.iloc[:,-1].sum())
        for cname in countryNameOptions:
            countryCumTotals = self.aggregateAllDataByCountryName(cname).iloc[-1,:]
            outputStr += """\\normalsize  {} && \\normalsize {:,} && \\normalsize {:,} && \\normalsize {:,} \\cr[2pt]""" \
                        .format(cname.upper(), countryCumTotals[0], countryCumTotals[1], countryCumTotals[2])
        outputStr += """\\end{matrix}"""
                        
                        
        return outputStr
    
    def getDailyCountsByCountry(self,option="confirmed", ncases=0):
        
        if(option=="confirmed"):
            outputDF = pd.DataFrame(self.confDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="recovered"):
            outputDF = pd.DataFrame(self.recoveredDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="deaths"):
            outputDF = pd.DataFrame(self.dtsDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="active"):
            outputDF = pd.DataFrame(self.activeDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        
        # drop rows below ncases
        outputDF = outputDF.drop(outputDF.index[outputDF.iloc[:,-1] < ncases])
               
        outputDF = outputDF.sort_values(by=outputDF.columns[-1], ascending=False)
        outputDF.columns = pd.to_datetime(outputDF.columns)
        
        return outputDF
    
    def getDailyNewCasesByCountry(self,option="confirmed", ncases=0):
        
        if(option=="confirmed"):
            outputDF = pd.DataFrame(self.confDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="recovered"):
            outputDF = pd.DataFrame(self.recoveredDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="deaths"):
            outputDF = pd.DataFrame(self.dtsDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="active"):
            outputDF = pd.DataFrame(self.activeDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        
        # drop rows below ncases
        outputDF = outputDF.drop(outputDF.index[outputDF.iloc[:,-1] < ncases])
       
       
        for icol in range(len(outputDF.columns)-1,0,-1):
            outputDF.iloc[:,icol] = (outputDF.iloc[:,icol] - outputDF.iloc[:,icol-1])
        
        
        outputDF = outputDF.sort_values(by=outputDF.columns[-1], ascending=False)
        outputDF.columns = pd.to_datetime(outputDF.columns)
        
        return outputDF
    
    def getDailyChangeRateByCountry(self,option="confirmed", ncases=0):
        
        if(option=="confirmed"):
            outputDF = pd.DataFrame(self.confDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="recovered"):
            outputDF = pd.DataFrame(self.recoveredDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="deaths"):
            outputDF = pd.DataFrame(self.dtsDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        if(option=="active"):
            outputDF = pd.DataFrame(self.activeDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"])
        
        # drop rows below ncases
        outputDF = outputDF.drop(outputDF.index[outputDF.iloc[:,-1] < ncases])
       
       
        for icol in range(len(outputDF.columns)-1,0,-1):
            outputDF.iloc[:,icol] = ((outputDF.iloc[:,icol] - outputDF.iloc[:,icol-1])/outputDF.iloc[:,icol-1])*100
        
        
        outputDF = outputDF.sort_values(by=outputDF.columns[-1], ascending=False)
        outputDF.columns = pd.to_datetime(outputDF.columns)
        
        return outputDF
    
    def getTopCountriesNewCasesGraph(self,option="confirmed",numCountries=5,numDays=0):
        
               
        fig = go.Figure()
        
        df = self.getDailyNewCasesByCountry(option)
        for irow in range(numCountries):
            fig.add_trace(
            go.Scatter(x=df.columns[-numDays:], y=df.iloc[irow, -numDays:], name=df.index[irow].upper(), line=dict(width=2), mode="lines+markers")
            )
        if(option=="confirmed"):
           fig.update_layout(
                title_text="Top " + str(numCountries) + " countries with new positive cases each day",
                legend=dict(orientation="h", yanchor="top", valign="middle", y=1.12)
            )
        if(option=="deaths"):
           fig.update_layout(
                title_text="Top " + str(numCountries) + " countries with new death cases each day",
                legend=dict(orientation="h", yanchor="top", valign="middle", y=1.12)
            )
        
        return fig
    
    def getTopCountriesActivePercent(self):
        cdf = self.getDailyCountsByCountry("confirmed")
        adf = self.getDailyCountsByCountry("active")
        
        
        countryNames = adf.index[adf>95]
        
        return countryNames
        
    # def getTopCountriesActivePercentGraph(self,numCountries=5,numDays=0):
    #     countryNames = self.getTopCountriesActivePercent()
        
    #     df = self.aggregateAllDataByCountryName(self.countryNames)
        
    #     df["active_percent"] = round((df["active"]/df["confirmed"])*100)
    #     df = df.sort_values(by="active_percent", ascending=False)
        
    #     countryNameOptions = df.index[df["active_percent"] > 95]
        
    #     for cname in range(countryNameOptions):
    #         fig.add_trace(
    #         go.Scatter(x=df.index, y=df.loc[countryNameOptions[cname]], name=cname, line=dict(width=2), mode="lines+markers")
    #         )
        
        
    
    def getContryHistogramGraph(self):
        
        df = self.getDailyCountsByCountry("confirmed")
        [freq, bins] = np.histogram(df.iloc[:,-1], bins=10)
        
        fig = make_subplots(rows=2, cols=2,subplot_titles=("Confirmed", "Deaths"))
        fig.add_trace(
            go.Bar(x=bins[1:], y=freq,  text=freq, textposition='outside'),
            row=1, col=1
        )
        fig.update_xaxes(title_text="cases", row=1, col=1)
        fig.update_yaxes(title_text="number of countries", row=1, col=1)
        
        df = self.getDailyCountsByCountry("deaths")
        [freq, bins] = np.histogram(df.iloc[:,-1], bins=10)
        fig.add_trace(
            go.Bar(x=bins[1:], y=freq,  text=freq, textposition='outside'),
            row=1, col=2
        )
        fig.update_xaxes(title_text="cases", row=1, col=2)
        fig.update_yaxes(title_text="number of countries",side='right', row=1, col=2)
                
        fig.update_layout(
            showlegend=False   
            )
        
        return fig
    
    def getCountryStatsGraph(self, countryName="canada"):
        numDays=60
        df = self.aggregateAllDataByCountryName(countryName)

        fig = go.Figure()
        colColors = ['#88F', '#0A3', '#F44', '#0AF']
        for icol in range(len(df.columns)):
            fig.add_trace(
            go.Scatter(x=df.index[-numDays:], y=df.iloc[-numDays:,icol], name=df.columns[icol], line=dict(width=2, color=colColors[icol]), mode="lines+markers")
            )
            
        
        # Add figure title
        fig.update_layout(
            title_text="Cumulative counts per day : " + countryName.upper()
        )
        fig.update_layout(
            legend=dict(
                x=0,
                y=1,
                traceorder="normal",
                font=dict(
                    family="sans-serif",
                    size=12,
                    color="black"
                ),
                bgcolor="LightSteelBlue",
                bordercolor="Black",
                #borderwidth=1
            )
        )
        
        # Set x-axis title
        #fig.update_xaxes(title_text="Date")
        
        return fig
    
    def getCountryRatesGraph(self, countryName="canada"):
        numDays=60
        df = self.aggregateAllDataByCountryName(countryName)

        fig = go.Figure()
        colColors = ['#88F', '#0A3', '#F44', '#0AF']
        for icol in range(1, len(df.columns)):
            fig.add_trace(
            go.Scatter(x=df.index[-numDays:], y=round((df.iloc[-numDays:,icol]/df.iloc[-numDays:,0])*100,2), 
                       name=df.columns[icol], line=dict(width=2, color=colColors[icol]), mode="lines+markers")
            )
            
        
        # Add figure title
        fig.update_layout(
            title_text="Ratios per day : " + countryName.upper()
        )
        fig.update_layout(
            legend=dict(
                x=0,
                y=1,
                traceorder="normal",
                font=dict(
                    family="sans-serif",
                    size=12,
                    color="black"
                ),
                bgcolor="LightSteelBlue",
                bordercolor="Black",
                #borderwidth=1
            )
        )
        
        
        return fig
    
    def getCountryNewCasesGraph(self,countryName="canada"):
        
        numDays = 60
        
        fig = make_subplots(rows=1, cols=2,subplot_titles=("Confirmed", "Deaths"))
        
        dfCounts = self.getDailyNewCasesByCountry("confirmed")
        fig.add_trace(
            go.Bar(x=dfCounts.columns[-numDays:], y=dfCounts.loc[countryName, dfCounts.columns[-numDays:]]),
            row=1, col=1
        )
        fig.update_yaxes(title_text="cases", row=1, col=1)
        
        dfCounts = self.getDailyNewCasesByCountry("deaths")
        fig.add_trace(
            go.Bar(x=dfCounts.columns[-numDays:], y=dfCounts.loc[countryName, dfCounts.columns[-numDays:]]),
            row=1, col=2
        )
        fig.update_yaxes(title_text="cases", side="right", row=1, col=2)
        
        fig.update_layout(
            title_text="New cases per day : " + countryName.upper(),
            showlegend=False   
            )        
        
        return fig
    
    
    

#myData = Covid19Data()
#myData.loadData()

# print(myData.getDailyCountsByCountry("confirmed"))
# print(myData.getDailyChangeRateByCountry("confirmed"))
# print(myData.getDailyNewCasesByCountry("deaths"))
#myData.getCountryNewCasesRatesGraph("India").show()
#myData.getTopCountriesActivePercentGraph(numCountries=5,numDays=45).show()