import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from packages.processing.Covid19Data import Covid19Data

    

# load data
myData = Covid19Data()
myData.loadData()

# display data

st.title("COVID 19 Dashboard")

countryName = st.selectbox("Select country name", 
                           myData.countryNames, 
                           int(myData.getCountryNameIndex("Canada"))
                           )

df = myData.aggregateAllDataByCountryName(countryName)


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


st.plotly_chart(fig)


