"""
Baylasan Innovation, Sudan
مخيم الوهمة،
Sudan/South Sudan Data,
Author(s): Rami Ahmed (KPI)
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

    html.Div([
        html.Div([
            dcc.Dropdown(id="slct_data",
                        options=[
                            {"label": "Population Density", "value": 'Population Density'},
                            {"label": "States Agro Sorting", "value": 'States Agro Sorting'},
                                ],
                        multi=False,
                        value='Population Density',
                        style={'width': "40%"},
                        clearable=False,
                        ),
                ],className='six columns'),

        html.Div([
            dcc.Dropdown(id='show_hide',
                        options=[
                                {'label': 'Show South Sudan', 'value': 'show'},
                                {'label': 'Hide  South Sudan', 'value': 'hide'}
                        ],
                        multi=False,
                        value='hide',
                        style={'width': "40%"},
                        clearable=False,
                        ),
                ],className='six columns'),

    ],className='row'),


    html.Br(),

    html.Div([
        dcc.Graph(id='my_data_map', figure={}),
        ],className='six columns')

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='my_data_map', component_property='figure'),
    [Input(component_id='slct_data', component_property='value'),
    Input(component_id='show_hide', component_property='value')]
)
def update_graph(slct_data, show_hide):

    if slct_data == 'Population Density':
        from popden import createfig
        fig = createfig(state_id_map, sudan, show_hide)

    elif slct_data == 'States Agro Sorting':
        from sorting import createfig
        fig = createfig(state_id_map, sudan, show_hide)


    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
