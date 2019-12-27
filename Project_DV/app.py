import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go

###################################################### Data Import ##############################################################

df = pd.read_csv('data/emission_full.csv')
df_refugees = pd.read_csv('data/refugees.csv')
gas_names = ['CO2_emissions', 'GHG_emissions', 'CH4_emissions','N2O_emissions', 'F_Gas_emissions']
places= ['energy_emissions', 'industry_emissions',
      'agriculture_emissions', 'waste_emissions',
       'land_use_foresty_emissions', 'bunker_fuels_emissions',
       'electricity_heat_emissions', 'construction_emissions',
       'transports_emissions', 'other_fuels_emissions']

######################################################Interactive Components############################################

country_options = [dict(label=country, value=country) for country in df['country_name'].unique()]

gas_options = [dict(label=gas.replace('_', ' '), value=gas) for gas in gas_names]
variable_refugee = ['Refugee population (by country/ territory of asylum)','Refugee population (by country/ territory of origin)']

refugees_options = [dict(label=variable, value=variable) for variable in variable_refugee]

sector_options = [dict(label=place.replace('_', ' '), value=place) for place in places]

##################################################APP###############################################################

app = dash.Dash(__name__)
app.layout = html.Div([

    html.Div([
        html.H1('Refugees, a Reality that Must be Faced and Understood'),
        html.H4('"Every day, all over the world, people make one of the most difficult decisions in their lives: to leave their homes in search of a safer, better life."')
    ], className='pretty'),

    html.Div([
        html.Div([
            dcc.Tabs(id='tabs',
                     value='tab_1',
                     children=[dcc.Tab(label='About', value='tab_1', children=[
                                                            html.Label('Country Choice'),
                                                                        dcc.Dropdown(
                                                                            id='country_drop',
                                                                            options=country_options,
                                                                            value=['Portugal'],
                                                                            multi=True
                                                                        ),

                                                                        html.Br(),

                                                                        html.Label('Gas Choice'),
                                                                        dcc.Dropdown(
                                                                            id='gas_option',
                                                                            options=refugees_options,
                                                                            value='Refugee population (by country/ territory of origin)',
                                                                        ),

                                                                        html.Br(),

                                                                        html.Label('Sector Choice'),
                                                                        dcc.Dropdown(
                                                                            id='sector_options',
                                                                            options=sector_options,
                                                                            value=['energy_emissions', 'waste_emissions'],
                                                                            multi=True
                                                                        ),

                                                                        html.Br(),
                                ]),
                               dcc.Tab(label='Data', value='tab_2', children=[
                                                        html.Label('Year Slider'),
                                                                    dcc.Slider(
                                                                        id='year_slider',
                                                                        min=df_refugees['Year'].min(),
                                                                        max=df_refugees['Year'].max(),
                                                                        marks={str(i): '{}'.format(str(i)) for i in [2009, 2010, 2011, 2012, 2013, 2014]},
                                                                        value=df_refugees['Year'].min(),
                                                                        step=1
                                                                    ),

                                                                    html.Br(),

                                                                    html.Label('Linear Log'),
                                                                    dcc.RadioItems(
                                                                        id='lin_log',
                                                                        options=[dict(label='Linear', value=0), dict(label='log', value=1)],
                                                                        value=0
                                                                    ),

                                                                    html.Br(),

                                                                    html.Label('Projection'),
                                                                    dcc.RadioItems(
                                                                        id='projection',
                                                                        options=[dict(label='Equirectangular', value=0), dict(label='Orthographic', value=1)],
                                                                        value=0
                                                                    )
                                ]),
                              ]),
            html.Button('Submit' ,id='Button')
        ], className='column1 pretty'),

        html.Div([

            html.Div([

                html.Div([html.Label(id='gas_1')], className='mini pretty'),
                html.Div([html.Label(id='gas_2')], className='mini pretty'),
                html.Div([html.Label(id='gas_3')], className='mini pretty'),
                html.Div([html.Label(id='gas_4')], className='mini pretty'),
                html.Div([html.Label(id='gas_5')], className='mini pretty'),

            ], className='5 containers row'),
            html.Div([dcc.Graph(id='choropleth')], className='column3 pretty'),

        ], className='column2')

    ], className='row'),

    html.Div([

        html.Div([dcc.Graph(id='scatter_graph')], className='column4 pretty'),
        html.Div([dcc.Graph(id='bar_graph')], className='column4 pretty')

    ], className='row')

])

###################################################### Callbacks #########################################################
@app.callback(
    [
        Output("choropleth", "figure")
    ],
    [
        Input('Button', 'n_clicks')
    ],
    [
        State("year_slider", "value"),
        State("gas_option", "value")
    ]
)
def plots(n_clicks, year,  gas):

    #############################################Choropleth######################################################

    df_emission_0 = df_refugees.loc[df_refugees['Year'] == year]
    df_sad = df_refugees
    z = np.log(df_emission_0[gas])

    data_choropleth = go.Choropleth(
                           locations=df_emission_0['Country Name'],
                           # There are three ways to 'merge' your data with the data pre embedded in the map
                           locationmode='country names',
                           z=z,
                           text=df_emission_0['Country Name'],
                           colorscale='RdYlGn',
                           colorbar=dict(title=dict(text=str(gas.replace('_', ' ')) + '<br> (log scaled)',
                                                    side='bottom'
                                                    ),
                                         x=1.02, xanchor='center'), #, , xref="container"

                           hovertemplate='Country: %{text} <br>' + str(gas.replace('_', ' ')) + ': %{z}',
                           name=''
                           )

    layout_choropleth = go.Layout(height=450,
                                    width=900,
                                    geo={'showframe':False, 'projection':{'type':'equirectangular'}},
                                  margin=go.layout.Margin(l=0, r=0, t=0, b=0)
                                  )

                             #title=dict(text='World ' + str(gas.replace('_', ' ')) + ' Choropleth Map on the year ' + str(year),
                             #           x=.5  # Title relative position according to the xaxis, range (0,1)

                               #         ),
                             #paper_bgcolor='#f9f9f9'
                             #)


    return go.Figure(data=data_choropleth, layout=layout_choropleth),\
           #go.Figure(data=data_bar, layout=layout_bar), \
           #go.Figure(data=data_agg, layout=layout_agg)


@app.callback(
    [
        Output("gas_1", "children"),
        Output("gas_2", "children"),
        Output("gas_3", "children"),
        Output("gas_4", "children"),
        Output("gas_5", "children")
    ],
    [
        Input("country_drop", "value"),
        Input("year_slider", "value"),
    ]
)
def indicator(countries, year):
    df_loc = df.loc[df['country_name'].isin(countries)].groupby('year').sum().reset_index()

    value_1 = round(df_loc.loc[df_loc['year'] == year][gas_names[0]].values[0], 2)
    value_2 = round(df_loc.loc[df_loc['year'] == year][gas_names[1]].values[0], 2)
    value_3 = round(df_loc.loc[df_loc['year'] == year][gas_names[2]].values[0], 2)
    value_4 = round(df_loc.loc[df_loc['year'] == year][gas_names[3]].values[0], 2)
    value_5 = round(df_loc.loc[df_loc['year'] == year][gas_names[4]].values[0], 2)

    return str(gas_names[0]).replace('_', ' ') + ': ' + str(value_1),\
           str(gas_names[1]).replace('_', ' ') + ': ' + str(value_2), \
           str(gas_names[2]).replace('_', ' ') + ': ' + str(value_3), \
           str(gas_names[3]).replace('_', ' ') + ': ' + str(value_4), \
           str(gas_names[4]).replace('_', ' ') + ': ' + str(value_5),


if __name__ == '__main__':
    app.run_server(debug=True)