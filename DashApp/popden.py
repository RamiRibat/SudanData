import numpy as np
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go


def loadData(state_id_map):
    GSID = '194VpZ8__NMRIyNGLRzN5css4xvSRYMfq6bv_JpblrEw'
    WSN = 'Data'
    URL = f"https://docs.google.com/spreadsheets/d/{GSID}/gviz/tq?tqx=out:csv&sheet={WSN}"
    df = pd.read_csv(URL)
    df["Density"] = df["Desity (ppkm²)"]
    df["Density Log Scale"] = np.round(np.log10(df["Density"]), 2)
    df["ID"] = df["State Name Ar"][:].apply(lambda x: list(state_id_map.keys())[list(state_id_map.values()).index(x)])
    dfsd = df.copy()
    dfss = df.copy()
    # Clear South Sudan's ID's:
    for i in range(0,len(df)):
        if df[i:i+1]['ID'][i].startswith('SS'):
            dfsd["State Name Ar"][i:i+1] = ''
    # Clear Sudan's ID's:
    for i in range(0,len(df)):
        if df[i:i+1]['ID'][i].startswith('SS') is False:
            dfss["State Name Ar"][i:i+1] = ''
    return dfsd, dfss


def createfig(state_id_map, sudan):

    dfsd, dfss = loadData(state_id_map)

    fig = px.choropleth(
    dfsd,
    locations="State Name Ar",
    geojson=sudan,
    color="Density Log Scale",
    title="Sudan/South sudan Population Density",
    width=1300, height=700
    ).update_geos(
        fitbounds="locations",
        visible=False).update_traces(
            hovertemplate=None
                            ).update_layout(
                    font={"color": "rgb(64,64,64)",
                        "family": "Times New Roman",
                        "size": 20},
                    titlefont={"color": "rgb(64,64,64)",
                            "family": "Times New Roman",
                            "size": 30})
    
    # add South Sudan
    fig.add_choropleth(
    autocolorscale=True,
    z=dfss["Density Log Scale"],
    locations=dfss["State Name Ar"],
    locationmode='geojson-id',
    geojson=sudan,
    showscale=False,
    marker=dict(opacity=0.5),
    hoverinfo='location+z'
                    ).update_traces(name='')

    return fig



