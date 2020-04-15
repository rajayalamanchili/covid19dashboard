import streamlit as st
# import plotly.graph_objects as go
# import plotly.express as px
# import numpy as np
# from plotly.subplots import make_subplots

from packages.processing.Covid19Data import Covid19Data

    

# load data
myData = Covid19Data()
myData.loadData()

# display data

st.title("COVID 19 Dashboard")
st.markdown("""###### Author: Raja Yalamanchili""")
st.markdown("""###### Data source: [Johns Hopkins CSSE data repository](https://github.com/CSSEGISandData/COVID-19)""")

#############################################################################
st.markdown("""---""")
countryNameOptions = st.multiselect("Select countries",
                                    myData.countryNames.tolist(),
                                    myData.getTopDailyNewCasesByCountry("confirmed").index.tolist())
                           

st.latex(myData.getCumulativeDataSummary(countryNameOptions))

#############################################################################
st.markdown("""---""")
st.plotly_chart(myData.getTopCountriesNewCasesGraph(option="confirmed",numCountries=5))
st.plotly_chart(myData.getTopCountriesNewCasesGraph(option="deaths",numCountries=5))

#st.plotly_chart(myData.getTopCountriesActivePercentGraph(numCountries=5,numDays=45))

#############################################################################
st.markdown("""---""")
counstOption = st.radio("Select an option", ("confirmed","active","recovered","deaths", "activeRatio", "recoveredRatio", "deathsRatio"),4)
st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.plotly_chart(myData.getGlobalCountsGraph(counstOption))

#############################################################################
st.markdown("""---""")
countryName = st.selectbox("Select country name", 
                           myData.countryNames, 
                           int(myData.getCountryNameIndex("canada"))
                           )

st.plotly_chart(myData.getCountryNewCasesGraph(countryName))
st.plotly_chart(myData.getCountryStatsGraph(countryName))
st.plotly_chart(myData.getCountryRatesGraph(countryName))

#############################################################################
#st.markdown("""---""")
#st.plotly_chart(myData.getContryHistogramGraph())



#############################################################################
# st.markdown("""---""")
# st.markdown("$\\scriptsize Data source:$ https://github.com/CSSEGISandData/COVID-19")


