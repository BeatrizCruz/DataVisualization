import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash.dependencies
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import math
from decimal import Decimal
import datetime
#import dash_dangerously_set_inner_html
# Import data set:
df_refugees = pd.read_csv('data/refugees.csv')

def munber_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def e_format(n):

    return '%.1E' % Decimal(n)

# App
app = dash.Dash(__name__)

country_options = [dict(label=country, value=country) for country in df_refugees['Country Name'].unique()]
variable_names = ['GDP per capita (US$)','Population (total)', 'Health Expenditure per capita (US$)', 'Life expectancy at birth','Military expenditure per capita (US$)', 'Unemployment (% of labor force)','Education Expenditure (per capita)']
variable_refugee = ['Refugees (asylum country)','Refugees (origin country)','Refugees per capita (by asylum country)','Refugees per capita (by origin country)']
allVar_names=['Refugees (asylum country)','Refugees (origin country)','GDP per capita (US$)', 'Population (total)', 'Health Expenditure per capita (US$)', 'Life expectancy at birth','Military expenditure per capita (US$)', 'Unemployment (% of labor force)','Education Expenditure (per capita)']
variable_options = [dict(label=variable, value=variable) for variable in variable_names]
refugees_options = [dict(label=variable, value=variable) for variable in variable_refugee]
allVar_options = [dict(label=variable, value=variable) for variable in allVar_names]
toplow_names= ['All Countries','Top 5','Top 10','Top 20','Low 5','Low 10','Low 20']
toplow_options=[dict(label=filtertop_low, value=filtertop_low) for filtertop_low in toplow_names]


app.layout = html.Div([

                    html.Div([
                        html.H1(['Refugees, a Reality that Must be Faced and Understood'], style={"font-family":"Verdana"}),
                        html.H4('"Every day, all over the world, people make one of the most difficult decisions in their lives: to leave their homes in search of a safer, better life."')
                    ], className='pretty'), #title

                    html.Div([
                        html.Div([
                            html.Div([
                                dcc.Tabs(id='tabs_info',
                                         value='tab_1',
                                         children=[
                                             dcc.Tab(label='Initial Considerations', value='tab_1', className= 'info', children=[
                                                html.Div([
                                                     html.Div([
                                                         html.H2('What is this App About?')], className='titleLeft'),
                                                     html.Div([
                                                         html.P([
                                                                '"We should all be aware that there are now more than 70 million refugees and internally displaced people across the world" (Jan Egeland, Euronews). The refugee crisis we face nowadays is huge and part of it derives from the lack of attention and responsibility formed by each country around this topic. '
                                                         ],className='text'),
                                                         html.P([
                                                                'The aim of this app is to give a first step towards the change of the current situation. We believe that, for people to get worried about this crisis, they first need to get informed. As visualizations are one of the best ways of representing data and transmitting it, we decided to develop this app. Therefore, this app’s objective is to present information about refugees’ movements reasons that'
                                                         ],className='text'),
                                                         html.P([
                                                                'Several observations might be taken concerning this app. The number of refugees leaving and arriving each country (movement variables) is easily accessed and might be compared with different social or economic variables for all countries in different years. For a more detailed analysis, each country might be studied over time.'
                                                         ],className='text'),
                                                         html.P([
                                                                'Through these observations many conclusions might be taken, such as the reasons why refugees go to specific countries or the countries that have good conditions and that could receive more refugees comparatively to the current received number.'
                                                         ],className='text'),
                                                     ]),
                                                     html.Div([html.H2('Who is a refugee?')], className='titleLeft'),
                                                     html.Div([
                                                         html.P([
                                                             'A refugee is a person who has fled their own country because they are at risk of serious human rights violations and persecution there. The risks to their safety and life were so great that they felt they had no choice but to leave and seek safety outside their country because their own government cannot or will not protect them from those dangers.'
                                                         ], className='text', style={"margin-bottom":"55px"}),
                                                     ]),
                                                     html.Div([
                                                        html.P(['A Project done by: Ana Oliveira, Beatriz Cruz, Ernesto, João Pimenta']),
                                                        dcc.Link('Click here for more information about refugees and if you want to help ', href='https://www.amnesty.org/en/what-we-do/refugees-asylum-seekers-and-migrants/')
                                                     ],style={"font-size":"10px", "margin-bottom":"0px"}),
                                                ], className='info'),
                                             ]),
                                             dcc.Tab(label='Data Information', value='tab_2', className= 'info', children=[
                                                html.Div([
                                                     html.Div([
                                                         html.P([
                                                             "All variables used on this app were taken from the World Bank. On this app, we use variables related with refugees’ movements and social- economic variables. All the used variables are from 2009 until 2018. "
                                                         ], className='text'),
                                                         html.H3(['Movement Variables'], className='titleLeft'),
                                                         html.Li([
                                                             "Refugee population (asylum): refugee population by country of asylum. Refugees under international protocols (asylum seekers are excluded). Country of asylum is the country where an asylum claim was filed and granted."
                                                         ], className='text'),
                                                         html.Li([
                                                             "Refugee population (origin): refugee population by country of origin. Country of origin generally refers to the nationality or country of citizenship of a claimant."
                                                         ], className='text'),
                                                         html.Li([
                                                             "Refugee population (asylum) per capita: Refugee population (asylum) divided by the total population number."
                                                         ], className='text'),
                                                         html.Li([
                                                             "Refugee population (origin) per capita: same as Refugee population (origin) divided by the total population number."
                                                         ], className='text'),
                                                         html.H3(['Socio- Economic Variables:'], className='titleLeft'),
                                                         html.Li([
                                                             "Population (total): total population is based on the de facto definition of population, which counts all residents regardless of legal status or citizenship."
                                                         ], className='text'),
                                                         html.Li([
                                                             "GDP per capita: Gross Domestic Product divided by midyear population. GDP is the sum of gross value added by all resident producers in the economy plus any product taxes and minus any subsidies not included in the value of the products. (US dollars)."
                                                         ], className='text'),
                                                         html.Li([
                                                             "Health Expenditure per capita: current expenditures on health per capita. Estimates of current health expenditures include healthcare goods and services consumed during each year. (US dollars)."
                                                         ], className='text'),
                                                         html.Li([
                                                             "Life expectancy at birth: The number of years a new born infant would live if prevailing patterns of mortality at the time of its birth were to stay the same throughout its life."
                                                         ], className='text'),
                                                         html.Li([
                                                             "Military expenditure per capita: Sum of capital expenditures on the armed forces, defense ministries and agencies, paramilitary forces, etc. Divided by the country's population. (US dollars)."
                                                         ], className='text'),
                                                         html.Li([
                                                             "Unemployment per capita: unemployment refers to the share of the labor force that is without work but available for and seeking employment. Divided by the country's population."
                                                         ], className='text'),
                                                         html.Li([
                                                             "Government expenditure on education: data may refer to spending by the ministry on education only. Divided by the country's population. (US dollars)"
                                                         ], className='text'),
                                                     ]),
                                                ], className='info'),
                                             ]),
                                             dcc.Tab(label='Data Display Choices', value='tab_3', children=[
                                                 html.Div([
                                                         html.H3('Map Options'),
                                                         html.Label('Choose a Refugee Variable:*\xB9 *\xB2 *\xB3'),
                                                         dcc.Dropdown(
                                                             id='refugee_options',
                                                             options=refugees_options,
                                                             value='Refugees (asylum country)',
                                                             multi=False,
                                                             clearable=False),
                                                        html.Br(),
                                                        html.Label('Choose a display scale:*\xB9'),
                                                        dcc.RadioItems(
                                                            id='lin_log',
                                                            options=[dict(label='Linear', value=0), dict(label='log', value=1)],
                                                            value=1, labelStyle={'display': 'inline-block'}),
                                                        html.Br(),
                                                        html.Label('Choose a year:*\xB9 *\xB2 *\u2074'),
                                                        dcc.Slider(
                                                            id='year_slider',
                                                            min=df_refugees['Year'].min(),
                                                            max=df_refugees['Year'].max(),
                                                            marks={str(i): '{}'.format(str(i)) for i in
                                                                  [2009, 2010, 2011, 2012, 2013, 2014,2015,2016,2017,2018]},
                                                            value=df_refugees['Year'].max(), included=False,
                                                            step=1),
                                                        html.Br(),
                                                        html.Button('Play/Stop', id='start', style={"width": "100%"}),
                                                        dcc.Interval(id='auto-stepper',
                                                                    interval=60*60*1000, # in milliseconds
                                                                    n_intervals=2008
                                                        ),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Label('Filter by top/low country values:*\xB9 *\xB2'),
                                                        dcc.Dropdown(
                                                            id='toplow_options',
                                                            options=toplow_options,
                                                            value='All Countries',
                                                            multi=False,
                                                            clearable=False
                                                        ),
                                                        html.Div([
                                                           html.Td(style={"width": "700px"}),
                                                         ], style={"width": "100%"}),
                                                        html.H3('Scatter plot Options'),
                                                        html.Label('Choose a Socio-economic variable:*\xB2 *\xB3'),
                                                        dcc.Dropdown(
                                                            id='exp_options',
                                                            options=variable_options,
                                                            value='GDP per capita (US$)',
                                                            multi=False,
                                                            clearable=False
                                                        ),
                                                        html.Div([
                                                            html.Td(style={"width": "700px"}),
                                                        ],style={"width": "100%"}),
                                                        html.H3('Line plot Options'),
                                                        html.Label('Choose a country:*\xB3 *\u2074'),
                                                        dcc.Dropdown(
                                                            id='country_drop',
                                                            options=country_options,
                                                            value='Portugal',
                                                            multi=False,
                                                            clearable=False),
                                                        html.Div([
                                                            html.Div([
                                                                html.P(['*\xB9'], style={"margin": "0px","padding": "0px"}),
                                                                html.P(['Changes choropleth map'],style={"margin": "2px 0px 0px 2px","font-size": "10px"}),
                                                            ], style={"margin": "0px","padding": "0px","display": "flex"}),
                                                            html.Div([
                                                                html.P(['*\xB2'], style={"margin": "0px","padding": "0px"}),
                                                                html.P([' Chanegs scatter plot'],style={"margin": "2px 0px 0px 2px","font-size": "10px"}),
                                                            ], style={"margin": "0px","margin-left": "7px","padding": "0px","display": "flex"}),
                                                            html.Div([
                                                                html.P(['*\xB3'], style={"margin": "0px","padding-bottom": "-3px"}),
                                                                html.P([' Changes line chart'],style={"margin": "2px 0px 0px 2px","font-size": "10px"}),
                                                            ],style={"margin": "0px","margin-left": "7px","display": "flex"}),
                                                            html.Div([
                                                                html.P(['*\u2074'], style={"margin": "0px","padding-bottom": "-3px"}),
                                                                html.P([' Changes info-cards'],style={"margin": "2px 0px 0px 2px","font-size": "10px"}),
                                                            ], style={"margin": "0px","margin-left": "7px","display": "flex"}),
                                                        ], style={"margin": "0px","padding": "0px","display": "flex"}),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Button('Refresh', id='refresh', style={"width": "100%","font-size": "10px"}),
                                                        html.P(id='time_refresh', style={"font-size": "10px", "margin-left":"1px", "margin-top":"3px"})


                                                 ], className='column30 info')

                                             ])
                                         ])
                            ]),

                        ],className='column30 pretty'),
                        html.Div([
                            html.Div([
                                html.Div([
                                    dcc.Graph(id='choropleth', style={"border": "1px solid lightgrey", "backgroundColor": "black"}),
                                ], className='pretty'),
                                html.Div([
                                    dcc.Graph(id='scatter_graph', style={"border": "1px solid lightgrey"})
                                ], className='pretty'),
                            ]),
                        ],className='column60'),
                    ],className='row'),




                    html.Div([
                        html.Div([dcc.Graph(id='line_graph', style={"border": "1px solid lightgrey"})], className='column60 pretty'),
                        html.Div([
                            html.Div([html.Label(id='var_1')], className='mini boxes'),
                            html.Div([html.Label(id='var_2')], className='mini boxes'),
                            html.Div([html.Label(id='var_3')], className='mini boxes'),
                            html.Div([html.Label(id='var_4')], className='mini boxes'),
                            html.Div([html.Label(id='var_5')], className='mini boxes'),
                            html.Div([html.Label(id='var_6')], className='mini boxes'),
                            html.Div([html.Label(id='var_7')], className='mini boxes'),
                            html.Div([html.Label(id='var_8')], className='mini boxes'),
                            html.Div([html.Label(id='var_9')], className='mini boxes', style={"margin-bottom": "0px"}),
                        ], className='column20'), # varios
                    ], className='row'),
                    html.Div([], style={"height":"900px"})
                ])




#
@app.callback(
    [
        Output("var_1", "children"),
        Output("var_2", "children"),
        Output("var_3", "children"),
        Output("var_4", "children"),
        Output("var_5", "children"),
        Output("var_6", "children"),
        Output("var_7", "children"),
        Output("var_8", "children"),
        Output("var_9", "children")

    ],
    [
        Input("country_drop", "value"),
        Input("year_slider", "value")
    ]
)

def indicator(countries, year):
    df_loc = df_refugees.loc[df_refugees['Country Name']==str(countries)]
    value_1 = round(df_loc.loc[df_loc['Year'] == year][allVar_names[0]].values[0], 2)
    value_2 = round(df_loc.loc[df_loc['Year'] == year][allVar_names[1]].values[0], 2)
    value_3 = round(df_loc.loc[df_loc['Year'] == year][allVar_names[2]].values[0], 2)
    value_4 = round(df_loc.loc[df_loc['Year'] == year][allVar_names[3]].values[0], 2)
    value_5 = round(df_loc.loc[df_loc['Year'] == year][allVar_names[4]].values[0], 2)
    value_6 = round(df_loc.loc[df_loc['Year'] == year][allVar_names[5]].values[0], 2)
    value_7 = round(df_loc.loc[df_loc['Year'] == year][allVar_names[6]].values[0], 2)
    value_8 = round(df_loc.loc[df_loc['Year'] == year][allVar_names[7]].values[0], 2)
    value_9 = round(df_loc.loc[df_loc['Year'] == year][allVar_names[8]].values[0], 2)

    return str(allVar_names[0])+': ' + str(munber_format(value_1)),\
           str(allVar_names[1])+': ' + str(munber_format(value_2)),\
           str(allVar_names[2])+': ' + str(munber_format(value_3)),\
           str(allVar_names[3])+': ' + str(munber_format(value_4)),\
           str(allVar_names[4])+': ' + str(munber_format(value_5)),\
           str(allVar_names[5])+': ' + str(munber_format(value_6)),\
           str(allVar_names[6])+': ' + str(munber_format(value_7)),\
           str(allVar_names[7])+': ' + str(munber_format(value_8)),\
           str(allVar_names[8])+': ' + str(munber_format(value_9))

#Run slider
@app.callback(
    dash.dependencies.Output('year_slider', 'value'),
    [dash.dependencies.Input('auto-stepper', 'n_intervals')])

def on_click(n_intervals):
    if n_intervals >= 2018:
        n_intervals = 2017
    print(n_intervals)
    if n_intervals is None:
        return 2018
    else:
        return n_intervals+1

#Start and Stop sliders
@app.callback([
                Output('auto-stepper', 'interval'),
                Output('auto-stepper', 'n_intervals')
              ],
              [
                Input('start', 'n_clicks')
              ])
def start_stop_interval(start):
    if start == None:
        return 60*60*1000, 2008
    else:
        if start%2 == 1:
            return 2*1000, 2008
        else:
            return 60*60*1000, 2008



#refresh plots
@app.callback(
    [
        Output("choropleth", "figure"),
        Output('scatter_graph','figure'),
        Output('line_graph','figure')
    ],
    [
        Input('lin_log','value'),
        Input("year_slider", "value"),
        Input("refugee_options", "value"),
        Input('exp_options','value'),
        Input('country_drop','value'),
        Input('toplow_options','value')
    ]
)


def plots(lin_log, year, var, exp, country,top_low):

    # Cloropleth:

    df_refugees_0 = df_refugees.loc[df_refugees['Year'] == year]
    if(lin_log==1):
        z2 = df_refugees_0[var]
        z = np.log(df_refugees_0[var])
        legend = '(logarithmic scale)'
        format_hover = ': %{z:.2f}'
        if var == 'Refugees per capita (by asylum country)' or var == 'Refugees per capita (by origin country)':
            legend_val = [-14,-12,-10,-8,-6,-4,-2,0]
            legend_text = ['-14 (' + e_format(math.exp(-14))+ ')','-12 (' + e_format(math.exp(-12))+ ')','-10 (' + e_format(math.exp(-10))+ ')','-8 (' + e_format(math.exp(-8))+ ')','-6 (' + e_format(math.exp(-6))+ ')','-4 (' + e_format(math.exp(-4))+ ')','-2 (' + e_format(math.exp(-2))+ ')', 0]
        else:
            legend_val = [0,2,4,6,8,10,12,14]
            legend_text= [0,'2 (' + munber_format(round(math.exp(2),0)) + ')','4 (' + munber_format(round(math.exp(4),0)) + ')','6 (' + munber_format(round(math.exp(6),0)) + ')','8 (' + munber_format(round(math.exp(8),0)) + ')','10 (' + munber_format(round(math.exp(10),0)) + ')','12 (' + munber_format(round(math.exp(12),0)) + ')','14 (' + munber_format(round(math.exp(14),0)) + ')']
    else:
        z = df_refugees_0[var]
        legend = '(linear scale)'
        legend_val = None
        legend_text = None
        if var == 'Refugees per capita (by asylum country)' or var == 'Refugees per capita (by origin country)':
            format_hover = ': %{z:8.7f}'
        else:
            format_hover = ': %{z}'


    if(top_low=='Top 5'):
        df_refugees_0 = df_refugees_0.sort_values(by=[var], ascending=False)
        countries = list(df_refugees_0.head(5)['Country Name'])
        df_refugees_0=df_refugees_0[df_refugees_0['Country Name'].isin(countries)]
    elif(top_low=='Top 10'):
        df_refugees_0 = df_refugees_0.sort_values(by=[var], ascending=False)
        countries = list(df_refugees_0.head(10)['Country Name'])
        df_refugees_0=df_refugees_0[df_refugees_0['Country Name'].isin(countries)]
    elif(top_low=='Top 20'):
        df_refugees_0 = df_refugees_0.sort_values(by=[var], ascending=False)
        countries = list(df_refugees_0.head(20)['Country Name'])
        df_refugees_0=df_refugees_0[df_refugees_0['Country Name'].isin(countries)]
    elif(top_low == 'Low 5'):
        df_refugees_0 = df_refugees_0.sort_values(by=[var], ascending=True)
        countries = list(df_refugees_0.head(5)['Country Name'])
        df_refugees_0=df_refugees_0[df_refugees_0['Country Name'].isin(countries)]
    elif (top_low == 'Low 10'):
        df_refugees_0 = df_refugees_0.sort_values(by=[var], ascending=True)
        countries = list(df_refugees_0.head(10)['Country Name'])
        df_refugees_0=df_refugees_0[df_refugees_0['Country Name'].isin(countries)]
    elif (top_low == 'Low 20'):
        df_refugees_0 = df_refugees_0.sort_values(by=[var], ascending=True)
        countries = list(df_refugees_0.head(20)['Country Name'])
        df_refugees_0=df_refugees_0[df_refugees_0['Country Name'].isin(countries)]
    # print(math.exp(10))
    # tickvals = [0, 2, 4, 6, 8, 10, 12, 14],
    # ticktext = [math.exp(0), math.exp(2), math.exp(4), math.exp(6), exp(8), exp(10), exp(12), exp(14)]

    data_choropleth = go.Choropleth(
                           locations=df_refugees_0['Country Name'],
                           # There are three ways to 'merge' your data with the data pre embedded in the map
                           locationmode='country names',
                           z=z,
                           text=df_refugees_0['Country Name'],
                           colorscale='RdYlGn',
                           reversescale=True,
                           colorbar=dict(title=dict(text=str(var) + '<br>'+ legend,
                                                    side='bottom',
                                                    ),
                                         tickvals=legend_val,
                                         ticktext=legend_text,
                                         x=-0.12, xanchor='left'),


                           hovertemplate='Country: %{text} <br>' + str(var) + format_hover,     #.format(z), #': %{z}.format()',
                           name=''
                           )

    layout_choropleth = go.Layout(#height=450,
                                  #width=900,
                                  geo={'showframe':False, 'projection':{'type':'equirectangular'}},
                                  margin=go.layout.Margin(l=0, r=0, t=0, b=0)

                                  )

    # Scatter Plot:
    data_scatter = go.Scatter(x=z,y=df_refugees_0[exp], mode='markers',text=df_refugees_0['Country Name'],
                            marker=dict(color=z, colorscale='RdYlGn', showscale=False))

    layout_scatter = go.Layout(title=str(exp)+' by '+str(var), xaxis=dict(title=str(var),showgrid=True),yaxis=dict(title=str(exp),showgrid=True),template=pio.templates['ggplot2'])
    # Bar Plot:
    df_refugees_1 = df_refugees.loc[df_refugees['Country Name'] == country]

    data_line = go.Scatter(x=df_refugees_1['Year'].values, y=df_refugees_1[exp],mode='lines+markers', name=str(exp), line=dict(color='rgb(201, 18, 18)'))
    layout_line = go.Layout(title=str(exp) + ' over years on '+country,  xaxis=dict(title='Year',showgrid=True), yaxis=dict(title=str(exp),showgrid=True),template=pio.templates['ggplot2'])
    line_graph = go.Figure(data=data_line, layout=layout_line)

    line_graph.add_trace(go.Scatter(x=df_refugees_1['Year'].values, y=df_refugees_1[var], mode='lines+markers', yaxis="y2", name=str(var), line=dict(color='rgb(5, 71, 176)')))
    line_graph.update_layout(yaxis2=dict(title=str(var), side="right", overlaying="y",showgrid=False), legend=dict(x=0.05, y=-.3), legend_orientation="h",hovermode='closest')

    fig = go.Figure(data=data_choropleth, layout=layout_choropleth)
    fig.update_layout(xaxis_tickformat='%')

    return fig,\
           go.Figure(data=data_scatter, layout=layout_scatter),\
           line_graph,

#refresh Datafram
@app.callback(
    # i'm imagining output as a hidden div, could be a dcc.Store or even user visible element
    Output("time_refresh", "children"),
    [Input("refresh", "n_clicks")],  # if refresh-data is a button maybe you want n_clicks not value?
)
def refresh_data(n_clicks):
    global df_refugees
    df_refugees = pd.DataFrame()
    df_refugees = pd.read_csv('data/refugees.csv')

    return 'Last dataset update: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    app.run_server(debug=True)
