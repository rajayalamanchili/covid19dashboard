import streamlit as st
# import plotly.graph_objects as go
# import plotly.express as px
# import numpy as np
# from plotly.subplots import make_subplots

from packages.processing.Covid19Data import Covid19Data

    
# display data

st.title("COVID 19 Dashboard")
st.markdown("""###### Author: Raja Yalamanchili""")
st.markdown("""###### Data source updated daily: [Johns Hopkins CSSE data repository](https://github.com/CSSEGISandData/COVID-19)""")



tabOptions = st.sidebar.selectbox("Select an option", ("GLOBAL", "CANADA PROVINCES"),0)



    

if (tabOptions=="GLOBAL"):
    # load data
    myData = Covid19Data()
    myData.loadData()

    #############################################################################
    st.markdown("""---""")
    countryNameOptions = st.multiselect("Select countries",
                                        myData.countryNames.tolist(),
                                        myData.getTopDailyNewCasesByCountry("confirmed").index.tolist())
                               
    
    st.latex(myData.getCumulativeDataSummary(countryNameOptions))
    
    #############################################################################
    st.markdown("""---""")
    
    daysOption = st.radio("", ("last 45 days","last 60 days","all days"),0)
    st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    myData.setNumDays(option=daysOption)
    
    st.plotly_chart(myData.getTopCountriesNewCasesGraph(option="confirmed",numCountries=5))
    st.plotly_chart(myData.getTopCountriesNewCasesGraph(option="deaths",numCountries=5))
    
    #st.plotly_chart(myData.getTopCountriesActivePercentGraph(numCountries=5,numDays=45))
    
    #############################################################################
    st.markdown("""---""")
    # recovery data discontinued after Aug 4, 2021
    countsOption = st.radio("Select an option", ("confirmed","deaths", "deathsRatio"),2)
    
    
    st.plotly_chart(myData.getGlobalCountsMap(countsOption))
    st.plotly_chart(myData.getGlobalCountsScatterPlot(countsOption))
    
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

if (tabOptions=="CANADA PROVINCES"):
    # load data
    myData = Covid19Data()
    myData.loadData()
    
    #############################################################################
    st.markdown("""---""")
    st.latex(myData.getCumulativeDataSummaryByProvince(countryName="canada"))
    #############################################################################
    st.markdown("""---""")
    daysOption = st.radio("", ("last 45 days","last 60 days","all"),0)
    st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    myData.setNumDays(option=daysOption)
    
    st.plotly_chart(myData.getProvincesNewCasesGraph(countryName="canada",option="confirmed"))
    st.plotly_chart(myData.getProvincesNewCasesGraph(countryName="canada",option="deaths"))
    #############################################################################
    st.markdown("""---""")
    countsOption = st.radio("Select an option", ("confirmed","deaths"),0)
        
    st.plotly_chart(myData.getProvinceCountsScatterPlot(countryName="canada", option=countsOption))
    st.plotly_chart(myData.getProvinceTimeScatterPlot(countryName="canada", option=countsOption))


