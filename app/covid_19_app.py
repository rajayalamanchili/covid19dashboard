import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

def aggregateAllDataByCountryName(inputDFConf,inputDFDTS,inputDFRecd,cname="Canada"):
    outputDF = pd.DataFrame(columns=["confirmed","deaths","recovered"])
    outputDF["confirmed"] = pd.DataFrame(inputDFConf.groupby("Country/Region").agg("sum")).drop(columns=["Lat","Long"]).transpose()[countryName]
    outputDF["deaths"] = pd.DataFrame(inputDFDTS.groupby("Country/Region").agg("sum")).drop(columns=["Lat","Long"]).transpose()[countryName]
    outputDF["recovered"] = pd.DataFrame(inputDFRecd.groupby("Country/Region").agg("sum")).drop(columns=["Lat","Long"]).transpose()[countryName]
    
    #outputDF = pd.DataFrame(inputDFConf.groupby("Country/Region").agg("sum")).drop(columns=["Lat", "Long"]).transpose()
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
countryConf = aggregateByCountry(inputDataConf)
countryDts = aggregateByCountry(inputDataDts)
countryRecd = aggregateByCountry(inputDataRecd)

countryName = st.selectbox("Select country name", 
                           countryConf.columns, 
                           countryConf.columns.get_loc("Canada")
                           )

df = aggregateAllDataByCountryName(inputDataConf,inputDataDts,inputDataRecd,countryName)


fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(x=df.index, y=df["confirmed"], name='confirmed'),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=df.index, y=df["deaths"], name='deaths'),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=df.index, y=df["recovered"], name='recovered'),
    secondary_y=False,
)

# Add figure title
fig.update_layout(
    title_text="COVID 19 STATS FOR : " + countryName
)

# Set x-axis title
fig.update_xaxes(title_text="Date")

# Set y-axes titles
#fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
#fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)
st.plotly_chart(fig)
