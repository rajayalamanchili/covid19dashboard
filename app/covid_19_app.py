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

st.markdown("""---""")

countryNameOptions = st.multiselect("Select upto 5 countries",
                                    myData.countryNames.tolist(),
                                    ["Canada", "US"])
                           

st.latex(myData.getCumulativeDataSummary(countryNameOptions))


st.markdown("""---""")
countryName = st.selectbox("Select country name", 
                           myData.countryNames, 
                           int(myData.getCountryNameIndex("Canada"))
                           )

df = myData.aggregateAllDataByCountryName(countryName)


fig = go.Figure()
colColors = ['#88F', '#0A3', '#F44']
for icol in range(len(df.columns)):
    fig.add_trace(
    go.Scatter(x=df.index[-30:], y=df.iloc[-30:,icol], name=df.columns[icol], line=dict(width=2, color=colColors[icol]), mode="lines+markers")
    )
    

# Add figure title
fig.update_layout(
    title_text="covid 19 counts last 30 days : " + countryName
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
fig.update_xaxes(title_text="Date")
st.plotly_chart(fig)

st.markdown("""---""")

df = myData.getDailyCountsByCountry("confirmed")
[freq, bins] = np.histogram(df.iloc[:,-1], bins=10)
fig = make_subplots(rows=1, cols=2,subplot_titles=("Confirmed", "Deaths"))
fig.add_trace(
    go.Bar(x=bins[1:], y=freq,  text=freq, textposition='outside'),
    row=1, col=1
)
fig.update_xaxes(title_text="cases", row=1, col=1)
fig.update_yaxes(title_text="number of countries", row=1, col=1)

df = myData.getDailyCountsByCountry("deaths")
[freq, bins] = np.histogram(df.iloc[:,-1], bins=10)
fig.add_trace(
    go.Bar(x=bins[1:], y=freq,  text=freq, textposition='outside'),
    row=1, col=2
)
fig.update_xaxes(title_text="cases", row=1, col=2)
fig.update_yaxes(title_text="number of countries",side='right', row=1, col=2)

fig.update_layout(
    showlegend=False,
    xaxis = dict(
            ticks="outside"            
        )
    )


st.plotly_chart(fig)

st.markdown("""---""")
st.markdown("$\\scriptsize Data source:$ https://github.com/CSSEGISandData/COVID-19")


