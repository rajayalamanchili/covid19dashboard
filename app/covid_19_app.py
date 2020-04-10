import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots

from packages.processing.Covid19Data import Covid19Data

    

# load data
myData = Covid19Data()
myData.loadData()

# display data

st.title("COVID 19 Dashboard")

#############################################################################
st.markdown("""---""")
st.plotly_chart(myData.getTopCountriesNewCasesGraph(option="confirmed",numCountries=5,numDays=30))
st.plotly_chart(myData.getTopCountriesNewCasesGraph(option="deaths",numCountries=5,numDays=30))


#############################################################################
st.markdown("""---""")
countryNameOptions = st.multiselect("Select upto 5 countries",
                                    myData.countryNames.tolist(),
                                    ["Canada", "US"])
                           

st.latex(myData.getCumulativeDataSummary(countryNameOptions))

#############################################################################
st.markdown("""---""")
countryName = st.selectbox("Select country name", 
                           myData.countryNames, 
                           int(myData.getCountryNameIndex("Canada"))
                           )

st.plotly_chart(myData.getCountryStatsGraph(countryName))
st.plotly_chart(myData.getCountryNewCasesRatesGraph(countryName))


#############################################################################
#st.markdown("""---""")
#st.plotly_chart(myData.getContryHistogramGraph())

#############################################################################
st.markdown("""---""")
st.markdown("$\\scriptsize Data source:$ https://github.com/CSSEGISandData/COVID-19")


