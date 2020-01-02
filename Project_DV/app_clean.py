import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import dash_dangerously_set_inner_html
# Import data set:
df_refugees = pd.read_csv('data/refugees.csv')
country_options = [dict(label=country, value=country) for country in df_refugees['Country Name'].unique()]
variable_names = ['GDP per capita (US$)','Population (total)', 'Health Expenditure per capita (US$)', 'Life expectancy at birth','Military expenditure per capita (US$)', 'Unemployment (% of labor force)','Education Expenditure (per capita)']
variable_refugee = ['Refugees (asylum country)','Refugees (origin country)','Refugees per capita (by asylum country)','Refugees per capita (by origin country)']
allVar_names=['Refugees (asylum country)','Refugees (origin country)','GDP per capita (US$)', 'Population (total)', 'Health Expenditure per capita (US$)', 'Life expectancy at birth','Military expenditure per capita (US$)', 'Unemployment (% of labor force)','Education Expenditure (per capita)']
variable_options = [dict(label=variable, value=variable) for variable in variable_names]
refugees_options = [dict(label=variable, value=variable) for variable in variable_refugee]
allVar_options = [dict(label=variable, value=variable) for variable in allVar_names]
toplow_names= ['All Countries','Top 5','Top 10','Top 20','Low 5','Low 10','Low 20']
toplow_options=[dict(label=filtertop_low, value=filtertop_low) for filtertop_low in toplow_names]

# App
app = dash.Dash(__name__)
app.layout = html.Div([

                    html.Div([
                        html.H1('Refugees, a Reality that Must be Faced and Understood'),
                        html.H4('"Every day, all over the world, people make one of the most difficult decisions in their lives: to leave their homes in search of a safer, better life."')
                    ], className='pretty'), #title

                    html.Div([
                        html.Div([
                            dcc.Tabs(id='tabs_info',
                                     value='tab_1',
                                     children=[
                                         dcc.Tab(label='Initial Considerations', value='tab_1', children=[
                                             html.Div([
                                                 html.H2('Why does this topic matter?')], className='titleLeft'),
                                             html.Div([
                                                          '“There are many reasons why people around the globe seek to rebuild their lives in a different country. Some people leave home to get a job or an education. Others are forced to flee persecution or human rights violations such as torture. Millions flee from armed conflicts or other crises or violence. Some no longer feel safe and might have been targeted just because of who they are or what they do or believe – for example, for their ethnicity, religion, sexuality or political opinions.'],
                                                      className='text'),

                                             html.Div([html.H2('Who is a refugee?')], className='titleLeft'),
                                             html.Div(
                                                 [
                                                     'A refugee is a person who has fled their own country because they are at risk of serious human rights violations and persecution there. The risks to their safety and life were so great that they felt they had no choice but to leave and seek safety outside their country because their own government cannot or will not protect them from those dangers.'
                                                 ], className='text'),

                                             html.Div([html.H2('Who is an asylum-seeker?')], className='titleLeft'),
                                             html.Div(
                                                 [
                                                     'An asylum-seeker is a person who has left their country and is seeking protection from persecution and serious human rights violations in another country, but who hasn’t yet been legally recognized as a refugee and is waiting to receive a decision on their asylum claim.'
                                                 ], className='text')

                                         ]),
                                         dcc.Tab(label='Data Information', value='tab_2', children=[
                                             html.Div([html.H2('What is this this app about?')], className='titleLeft'),
                                             html.Div(
                                                 [
                                                     "Our objective with the development of this app was to, first of all, present information about the amount of refugees leaving and arriving on each country over the years (from 2009 to 2016). Secondly, we intended to explain refugees' movements through social and economic variables. We found that an interactive visualization would be the best option to represent all this information in a simple and effective way."
                                                 ], className='text'),
                                             html.H2('Movement Variables:'),
                                             html.H2(
                                                 '- Refugee population (by country of origin): Number of refugees leaving each country.'),
                                             html.H2('- Refugee population (by country of asylum): '),
                                             html.Div(
                                                 [
                                                     "Number of refugees arriving each country seeking for asylum."
                                                 ], style={"textAlign": "center"}),
                                             html.H3('Social-Economic Variables:'),
                                             html.Div(
                                                 [
                                                     ""
                                                 ], style={"textAlign": "center"})
                                         ]),
                                         dcc.Tab(label='Data Display Choices', value='tab_3', children=[
                                             html.Div([
                                                     html.H3('Map Options:'),
                                                     html.Label('Choose a Refugee Variable:'),
                                                     dcc.Dropdown(
                                                         id='refugee_options',
                                                         options=refugees_options,
                                                         value='Refugees (asylum country)',
                                                         multi=False,
                                                         clearable=False),
                                                    html.Br(),

                                                    html.Label('Year Slider'),
                                                    dcc.Slider(
                                                        id='year_slider',
                                                        min=df_refugees['Year'].min(),
                                                        max=df_refugees['Year'].max(),
                                                        marks={str(i): '{}'.format(str(i)) for i in
                                                              [2009, 2010, 2011, 2012, 2013, 2014,2015,2016,2017,2018]},
                                                        value=df_refugees['Year'].max(),
                                                        step=1),
                                                    html.Br(),
                                                    html.Label('Do you want a Linear or a Logarithmic display?'),
                                                    dcc.RadioItems(
                                                        id='lin_log',
                                                        options=[dict(label='Linear', value=0), dict(label='log', value=1)],
                                                        value=1, labelStyle={'display': 'inline-block'}),
                                                    html.Br(),

                                                    html.Label('Do you want to filter by top/ low valued countries?'),
                                                    dcc.Dropdown(
                                                        id='toplow_options',
                                                        options=toplow_options,
                                                        value='All Countries',
                                                        multi=False,
                                                        clearable=False
                                                    ),
                                                    html.Br(),

                                                    html.H4('Scatter plot Options:'),

                                                    html.Label('Choose a Social-economical Variable:'),
                                                    dcc.Dropdown(
                                                        id='exp_options',
                                                        options=variable_options,
                                                        value='GDP per capita (US$)',
                                                        multi=False,
                                                        clearable=False
                                                   ),

                                                    html.Br(),

                                                    html.H4('Line plot Options:'),

                                                    html.Label('Country Choice'),
                                                    dcc.Dropdown(
                                                        id='country_drop',
                                                        options=country_options,
                                                        value='Portugal',
                                                        multi=False,
                                                        clearable=False),
                                                    html.Br(),


                                            ], className='column30 pretty')

                                                 ])
                                     ])
                                ],className='column30 pretty'),
                        html.Div([
                                dcc.Graph(id='choropleth'),
                                dcc.Graph(id='scatter_graph')
                                ], className='column60 pretty')
                            ],className='pretty row'), #info

                    html.Div([
                        html.Div([

                            html.Div([dcc.Graph(id='line_graph')], className='column60 pretty'),
                            html.Div([
                                html.Div([html.Label(id='var_1')], className='mini boxes'),
                                html.Div([html.Label(id='var_2')], className='mini boxes'),
                                html.Div([html.Label(id='var_3')], className='mini boxes'),
                                html.Div([html.Label(id='var_4')], className='mini boxes'),
                                html.Div([html.Label(id='var_5')], className='mini boxes'),
                                html.Div([html.Label(id='var_6')], className='mini boxes'),
                                html.Div([html.Label(id='var_7')], className='mini boxes'),
                                html.Div([html.Label(id='var_8')], className='mini boxes'),
                                html.Div([
                                    html.P(['A Project done by:'],className='bold'),
                                    html.Div('Ana Oliveira'),
                                    html.Div('Beatriz Cruz'),
                                    html.Div('Ernesto'),
                                    html.Div('João Pimenta')],className='mini boxes')
                                    ], className='column20') # varios
                                ], className='row') #row2
                ])
])

@app.callback(
    [
        Output("var_1", "children"),
        Output("var_2", "children"),
        Output("var_3", "children"),
        Output("var_4", "children"),
        Output("var_5", "children"),
        Output("var_6", "children"),
        Output("var_7", "children"),
        Output("var_8", "children")

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

    return str(allVar_names[0])+': ' + str(value_1),\
           str(allVar_names[1])+': ' + str(value_2),\
           str(allVar_names[2])+': ' + str(value_3),\
           str(allVar_names[3])+': ' + str(value_4),\
           str(allVar_names[4])+': ' + str(value_5),\
           str(allVar_names[5])+': ' + str(value_6),\
           str(allVar_names[6])+': ' + str(value_7),\
           str(allVar_names[7])+': ' + str(value_8)\

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
        z = np.log(df_refugees_0[var])
        legend = '(logarithmic scale)'
    else:
        z = df_refugees_0[var]
        legend = '(linear scale)'

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

    data_choropleth = go.Choropleth(
                           locations=df_refugees_0['Country Name'],
                           # There are three ways to 'merge' your data with the data pre embedded in the map
                           locationmode='country names',
                           z=z,
                           text=df_refugees_0['Country Name'],
                           colorscale='RdYlGn',
                           # colorscale=[[0.0,'rgb(32, 74, 48)'], [0.0625,'rgb(44, 120, 73)'],
                           #              [0.125,'rgb(38, 130, 39)'], [0.1875,'rgb(45, 189, 64)'],
                           #               [0.25, 'rgb(155, 189, 45)'], [0.3125,'rgb(192, 204, 27)'],
                           #               [0.375, 'rgb(212, 224, 36)'], [0.4375,'rgb(234, 247, 37)'],
                           #               [0.5,'rgb(251, 255, 0)'], [0.5625,'rgb(255, 208, 0)'],
                           #               [0.625,'rgb(255, 179, 0)'],[0.6875,'rgb(255, 153, 0)'],
                           #               [0.75,'rgb(255, 119, 0)'],[0.8125,'rgb(255, 98, 0)'],
                           #               [0.875,'rgb(255, 77, 0)'],[0.9375,'rgb(255, 0, 0)'],[1,'rgb(255, 0, 0)']],
                           # colorscale=[[0.0, 'rgb(44, 120, 73)'],[0.0417, 'rgb(38, 130, 39)'],
                           #             [0.0834, 'rgb(45, 189, 64)'],[0.1251, 'rgb(155, 189, 45)'],
                           #             [0.1668, 'rgb(234, 247, 37)'],[0.2085, 'rgb(224, 177, 36)'], #Stop
                           #             [0.25, 'rgb(224, 152, 36)'],[0.625, 'rgb(255, 153, 0)'],[1, 'rgb(255, 0, 0)']],
                           # colorscale=[[0.0, 'rgb(32, 74, 48)'], [0.029, 'rgb(44, 163, 90)'],
                           #             [0.058, 'rgb(52, 189, 45)'], [0.087, 'rgb(195, 214, 51)'],
                           #             [0.116, 'rgb(250, 250, 0)'], [0.145, 'rgb(224, 177, 36)'],
                           #             [0.174, 'rgb(224, 152, 36)'], [0.625, 'rgb(255, 153, 0)'], [1, 'rgb(255, 0, 0)']],
                           reversescale=True,
                           colorbar=dict(title=dict(text=str(var) + '<br>'+ legend,
                                                    side='bottom'
                                                    ),
                                         x=-0.12, xanchor='left'), #, , xref="container"

                           hovertemplate='Country: %{text} <br>' + str(var) + ': %{z}',
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

    data_line = go.Scatter(x=df_refugees_1['Year'].values, y=df_refugees_1[exp],mode='lines', name=str(exp), line=dict(color='rgb(201, 18, 18)'))
    layout_line = go.Layout(title=str(exp) + ' over years on '+country,  xaxis=dict(title='Year',showgrid=True), yaxis=dict(title=str(exp),showgrid=True),template=pio.templates['ggplot2'])
    line_graph = go.Figure(data=data_line, layout=layout_line)

    line_graph.add_trace(go.Scatter(x=df_refugees_1['Year'].values, y=df_refugees_1[var], mode='lines', yaxis="y2", name=str(var), line=dict(color='rgb(24, 112, 24)')))
    line_graph.update_layout(yaxis2=dict(title=str(var), side="right", overlaying="y",showgrid=False), legend=dict(x=0.05, y=-.3), legend_orientation="h",hovermode='closest')

    return go.Figure(data=data_choropleth, layout=layout_choropleth),\
           go.Figure(data=data_scatter, layout=layout_scatter),\
           line_graph,


if __name__ == '__main__':
    app.run_server(debug=True)


