"""
Baylasan Innovation, Sudan
مخيم الوهمة،
Sudan/South Sudan Data,
Author(s): Rami Ahmed (KPI)
"""

import numpy as np
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go


def loadData(state_id_map):
    GSID = '13ot0rYLxegd-JxNBXjcF1obxwPzhl99sKSGICJpINiY'
    WSN = 'StatesPoints'
    URL = f'https://docs.google.com/spreadsheets/d/{GSID}/gviz/tq?tqx=out:csv&sheet={WSN}'
    df = pd.read_csv(URL)
    df['ID'] = df["الولاية"].apply(lambda x: list(state_id_map.keys())[list(state_id_map.values()).index(x)])
    dfsd = df.copy()
    dfss = df.copy()
    # Clear South Sudan's ID's:
    for i in range(0,len(df)):
        if df[i:i+1]['ID'][i].startswith('SS'):
            dfsd['الولاية'][i:i+1] = ''
    # Clear Sudan's ID's:
    for i in range(0,len(df)):
        if df[i:i+1]['ID'][i].startswith('SS') is False:
            dfss['الولاية'][i:i+1] = ''

    return df, dfsd, dfss


def createfig(state_id_map, sudan, show_hide):

    df, dfsd, dfss = loadData(state_id_map)

    fig = px.choropleth(
    dfsd,
    locations='الولاية', # From DF --> GeoJson id map
    geojson=sudan,
    color="النقاط",
    title="ترتيب الولايات حسب الجاهزية",
    color_continuous_scale=px.colors.diverging.RdYlGn,
    width=1200, height=800
    ).update_geos(
        fitbounds="locations",
        visible=False).update_traces(
            hovertemplate=None).update_layout(
                    font={"color": "rgb(64,64,64)",
                        "family": "Times New Roman",
                        "size": 20},
                    titlefont={"color": "rgb(64,64,64)",
                            "family": "Times New Roman",
                            "size": 30})

    # Create Data for Top 3 States
    dfsd_top = dfsd.copy()
    # Clear points less than top 3:
    for i in range(0,len(dfsd)):
        if dfsd[i:i+1]["النقاط"][i] < dfsd.nlargest(3, "النقاط")["النقاط"].min():
            dfsd_top = dfsd_top.drop([i])
    
    dfsd_top = dfsd_top.sort_values('النقاط',ascending=False)

    # Star Top 3 States:
    fig.add_scattergeo(
        locations=dfsd_top["الولاية"],
        geojson=sudan,
        text=dfsd_top["الولاية"],
        textfont = {"color": "rgb(32,32,32)",
                    "family": "Arial, Bold",
                    "size": 20},
        textposition="bottom center",
        marker= dict(size=[30,25,20],
                    color=['Gold', 'Silver', 'Brown'],
                    opacity=1,
                    symbol='star'
                    ),
        mode ="markers+text",
        showlegend=False,
        hoverinfo='skip'
    )

    # Add South Sudan
    if show_hide == 'show':
        # Make South Sudan Points Nuetral
        for i in range(0,len(df)):
            if df[i:i+1]['ID'][i].startswith('SS') is True:
                dfss["النقاط"][i:i+1] = (df["النقاط"].min() + df["النقاط"].max())/2

        fig.add_choropleth(
        autocolorscale=False,
        z=dfss["النقاط"],
        locations=dfss["الولاية"],
        locationmode='geojson-id',
        geojson=sudan,
        showscale=False,
        marker=dict(opacity=0.5),
        hoverinfo='location'
                        ).update_traces(name='')

    return fig


