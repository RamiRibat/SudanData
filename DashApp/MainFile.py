"""
Baylasan Innovation, Sudan
مخيم الوهمة،
Sudan/South Sudan Data,
Author(s): Rami Ahmed
"""

import json

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

# ------------------------------------------------------------------------------
# Load GeoJson file for Sudan/South Sudan's States
sudan = json.load(open("SD_SSD_States.geojson", "r"))
state_id_map = {}
for feature in sudan["features"]:
    feature["id"] = feature["properties"]["StateNameAr"]
    state_id_map[feature["properties"]["StateID"]] = feature["id"]


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Sudan, South Sudan Data", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_data",
                 options=[
                     {"label": "Population Density", "value": 'Population Density'},
                     {"label": "States Agro Sorting", "value": 'States Agro Sorting'},
                        ],
                 multi=False,
                 value='Population Density',
                 style={'width': "40%"}
                 ),

    # html.Div(id='output_container', children=[]),
    html.Br(),

    html.Div([
        dcc.Graph(id='my_data_map', figure={}),
        ],className='six columns')

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    # [Output(component_id='output_container', component_property='children'),
    Output(component_id='my_data_map', component_property='figure'),#],
    Input(component_id='slct_data', component_property='value')
)
def update_graph(option_slctd):
    # print(option_slctd)
    # print(type(option_slctd))

    # container = "The Data chosen by user was: {}".format(option_slctd)

    if option_slctd == 'Population Density':
        from popden import createfig
        fig = createfig(state_id_map, sudan)

    elif option_slctd == 'States Agro Sorting':
        from sorting import createfig
        fig = createfig(state_id_map, sudan)


    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
