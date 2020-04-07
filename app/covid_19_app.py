import streamlit as st
import plotly.graph_objects as go
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


fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(x=df.index[-30:], y=df.iloc[-30:,0], name='confirmed'),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df.index[-30:], y=df.iloc[-30:,2], name='deaths'),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=df.index[-30:], y=df.iloc[-30:,1], name='recovered'),
    secondary_y=False,
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
st.markdown("***Data source:*** https://github.com/CSSEGISandData/COVID-19")


