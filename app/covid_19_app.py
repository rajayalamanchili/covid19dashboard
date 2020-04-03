import streamlit as st
import pandas as pd
import numpy as np
#import plotly.express as px

url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
fnames = ("time_series_covid19_confirmed_global.csv","time_series_covid19_deaths_global.csv","time_series_covid19_recovered_global.csv")

# load data
inputDataConf = pd.read_csv(url + fnames[0])
inputDataDts = pd.read_csv(url + fnames[1])
inputDataRecd = pd.read_csv(url + fnames[2])

# process data
def aggregateByCountry(inputDF):
    
    outputDF = pd.DataFrame(inputDF.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"]).transpose()
    outputDF.index = pd.to_datetime(outputDF.index)
    
    return outputDF

def aggregateLatestByCountry(inputDF):
    
    outputDF = pd.DataFrame(inputDataConf.groupby("Country/Region")[inputDataConf.columns[-1]].agg("sum"))
    outputDF.rename(columns={outputDF.columns[-1]:"latest"}, inplace=True)
    outputDF["Lat"] = inputDataConf.groupby("Country/Region")["Lat"].agg("mean")
    outputDF["Long"] = inputDataConf.groupby("Country/Region")["Long"].agg("mean")
    outputDF = outputDF.reset_index()
    
    return outputDF
    


dateRange = inputDataConf.columns[4:]

# display data

st.title("COVID 19 Dashboard")
st.text("Select a country name")
countryConf = aggregateByCountry(inputDataConf)
countryDts = aggregateByCountry(inputDataDts)
countryRecd = aggregateByCountry(inputDataRecd)

countryName = st.selectbox("Select country name", 
                           countryConf.columns, 
                           countryConf.columns.get_loc("Canada")
                           )

st.text("Confirmed")
st.line_chart(countryConf[countryName])

st.text("Deaths")
st.line_chart(countryDts[countryName])

st.text("Recovered")
st.line_chart(countryRecd[countryName])

# countryLatestConf = aggregateLatestByCountry(inputDataConf)
# countryLatestConf = countryLatestConf[["Long", "Lat"]]
# countryLatestConf.columns = ["lon", "lat"]
# st.map(countryLatestConf)
