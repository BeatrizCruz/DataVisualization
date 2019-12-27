import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# Import data set:
df_refugees = pd.read_csv('data/refugees.csv')
country_options = [dict(label=country, value=country) for country in df_refugees['Country Name'].unique()]
variable_names = ['GDP per capita (current US$)', 'Health Expenditure per capita (current US$)', 'Life expectancy at birth (total years)','Military expenditure per capita (current US$)', 'Unemployment per capita','Government expenditure on education (per capita)']
variable_refugee = ['Refugee population (by country/ territory of asylum)','Refugee population (by country/ territory of origin)']
allVar_names=['Refugee population (by country/ territory of asylum)','Refugee population (by country/ territory of origin)','GDP per capita (current US$)', 'Health Expenditure per capita (current US$)', 'Life expectancy at birth (total years)','Military expenditure per capita (current US$)', 'Unemployment per capita','Government expenditure on education (per capita)']
variable_options = [dict(label=variable, value=variable) for variable in variable_names]
refugees_options = [dict(label=variable, value=variable) for variable in variable_refugee]
allVar_options = [dict(label=variable, value=variable) for variable in allVar_names]


# App
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
                                     children=[
                                               dcc.Tab(label='Initial Considerations', value='tab_1', children=[
                                                                                                html.Div([
                                                                                                    html.H2('Why does this topic matter?')],className='titleLeft'),
                                                                                                html.Div(['“There are many reasons why people around the globe seek to rebuild their lives in a different country. Some people leave home to get a job or an education. Others are forced to flee persecution or human rights violations such as torture. Millions flee from armed conflicts or other crises or violence. Some no longer feel safe and might have been targeted just because of who they are or what they do or believe – for example, for their ethnicity, religion, sexuality or political opinions.'],className='text'),
                                                                                                html.Div(['There are many reasons why people around the globe seek to rebuild their lives in a different country. Some people leave home to get a job or an education. Others are forced to flee persecution or human rights violations such as torture. Millions flee from armed conflicts or other crises or violence. Some no longer feel safe and might have been targeted just because of who they are or what they do or believe – for example, for their ethnicity, religion, sexuality or political opinions.'], className='text'),
                                                                                                html.Div(['These journeys, which all start with the hope for a better future, can also be full of danger and fear. Some people risk falling prey to human trafficking and other forms of exploitation. Some are detained by the authorities as soon as they arrive in a new country. Once they’re settling in and start building a new life, many face daily racism, xenophobia and discrimination.'], className='text'),
                                                                                                html.Div(['Some people end up feeling alone and isolated because they have lost the support networks that most of us take for granted – our communities, colleagues, relatives and friends."'], className='text'),
                                                                                                html.Div(['The refugee topic should be everyone’s concern. If we can help building a better world, where there are fewer people suffering and struggling with serious problems as the ones described above, why don’t we? Fighting for the human rights is crucial. The consumer world needs to wake up and start solving real problems.'], className='text'),
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
                                                                                                html.Div([html.H2('What is this this app about?')],className='titleLeft'),
                                                                                                html.Div(
                                                                                                [
                                                                                                "Our objective with the development of this app was to, first of all, present information about the amount of refugees leaving and arriving on each country over the years (from 2009 to 2016). Secondly, we intended to explain refugees' movements through social and economic variables. We found that an interactive visualization would be the best option to represent all this information in a simple and effective way."
                                                                                                ], className='text'),
                                                                                                html.H2('Movement Variables:'),
                                                                                                html.H2('- Refugee population (by country of origin): Number of refugees leaving each country.'),
                                                                                                html.H2('- Refugee population (by country of asylum): '),
                                                                                                html.Div(
                                                                                                [
                                                                                                "Number of refugees arriving each country seeking for asylum."
                                                                                                ], style={ "textAlign": "center"}),
                                                                                                html.H3('Social-Economic Variables:'),
                                                                                                html.Div(
                                                                                                [
                                                                                                ""
                                                                                                ], style={ "textAlign": "center"})
                                                                                             ]),
                                               dcc.Tab(label='Data Display', value='tab_3', children=[html.Label('Year Slider'),
                                                                                           dcc.Slider(
                                                                                               id='year_slider',
                                                                                               min=df_refugees['Year'].min(),
                                                                                               max=df_refugees['Year'].max(),
                                                                                               marks={str(i): '{}'.format(str(i)) for i in
                                                                                                      [2009, 2010, 2011, 2012, 2013, 2014]},
                                                                                               value=df_refugees['Year'].max(),
                                                                                               step=1),
                                                                                           html.Br(),
                                                                                           html.Label('Country Choice'),
                                                                                           dcc.Dropdown(
                                                                                                id='country_drop',
                                                                                                options=country_options,
                                                                                                value='Portugal',
                                                                                                multi=False,
                                                                                                clearable=False),
                                                                                           html.Br(),
                                                                                           html.Label('Do you want a Linear or a Logarithmic display?'),
                                                                                           dcc.RadioItems(
                                                                                                id='lin_log',
                                                                                                options=[dict(label='Linear', value=0), dict(label='log', value=1)],
                                                                                                value=1),
                                                                                           html.Br(),
                                                                                           html.Label('Choose a Refugee Variable:'),
                                                                                           dcc.Dropdown(
                                                                                                id='refugee_options',
                                                                                                options=refugees_options,
                                                                                                value='Refugee population (by country/ territory of asylum)',
                                                                                                multi=False,
                                                                                                clearable=False),
                                                                                           html.Br(),
                                                                                           html.Label('Choose a Social-economical Variable:'),
                                                                                           dcc.Dropdown(
                                                                                                id='exp_options',
                                                                                                options=variable_options,
                                                                                                value='GDP per capita (current US$)',
                                                                                                multi=False,
                                                                                                clearable=False
                                                                                            )

                                                    ]),
                                     ]),

                        ], className='column1 pretty'),

                    html.Div([
                        html.Div([
                            html.Div([html.Label(id='var_1')], className='mini pretty'),
                            html.Div([html.Label(id='var_2')], className='mini pretty'),
                            html.Div([html.Label(id='var_3')], className='mini pretty'),
                            html.Div([html.Label(id='var_4')], className='mini pretty'),
                            html.Div([html.Label(id='var_5')], className='mini pretty'),
                            html.Div([html.Label(id='var_6')], className='mini pretty'),
                            html.Div([html.Label(id='var_7')], className='mini pretty'),
                            html.Div([html.Label(id='var_8')], className='mini pretty')

                            ], className='8 containers row'),
                        html.Div([dcc.Graph(id='choropleth')], className='column3 pretty'),
                        ], className='column2')

                    ], className='row'),
                    html.Div([
                        html.Div([dcc.Graph(id='scatter_graph')], className='column4 pretty'),
                        html.Div([dcc.Graph(id='bar_graph')], className='column4 pretty')
                        ], className='row')
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
        Output('bar_graph','figure')
    ],
    [
        Input('lin_log','value'),
        Input("year_slider", "value"),
        Input("refugee_options", "value"),
        Input('exp_options','value'),
        Input('country_drop','value')
    ]
)

def plots(lin_log, year, var,exp, country):
    # Cloropleth:
    df_refugees_0 = df_refugees.loc[df_refugees['Year'] == year]
    if(lin_log==1):
        z = np.log(df_refugees_0[var])
        legend = '(logarithmic scale)'
    else:
        z = df_refugees_0[var]
        legend = '(linear scale)'
    data_choropleth = go.Choropleth(
                           locations=df_refugees_0['Country Name'],
                           # There are three ways to 'merge' your data with the data pre embedded in the map
                           locationmode='country names',
                           z=z,
                           text=df_refugees_0['Country Name'],
                           colorscale='RdYlGn',

                           colorbar=dict(title=dict(text=str(var) + '<br>'+ legend,
                                                    side='bottom'
                                                    ),
                                         x=1.02, xanchor='center'), #, , xref="container"

                           hovertemplate='Country: %{text} <br>' + str(var) + ': %{z}',

                           name=''
                           )

    layout_choropleth = go.Layout(height=450,
                                  width=900,
                                  geo={'showframe':False, 'projection':{'type':'equirectangular'}},
                                  margin=go.layout.Margin(l=0, r=0, t=0, b=0)
                                  )
    # Scatter Plot:
    data_scatter = go.Scatter(x=z,y=df_refugees_0[exp], mode='markers',text=df_refugees_0['Country Name'],
                            marker=dict(color=z, colorscale='RdYlGn', showscale=False))
    layout_scatter = go.Layout(title=str(exp)+' by '+str(var), scene=dict(xaxis=dict(title=str(var)),
                                                                      yaxis=dict(title=str(exp))))
    # Bar Plot:
    df_refugees_1 = df_refugees.loc[df_refugees['Country Name'] == country]

    data_bar = go.Scatter(x=df_refugees_1['Year'].values, y=df_refugees_1[exp],mode='lines')
    layout_bar = go.Layout(title=str(exp) + ' over years for '+country, scene=dict(xaxis=dict(title='Year'),
                                                                                   yaxis=dict(title=exp)))
    return go.Figure(data=data_choropleth, layout=layout_choropleth),\
           go.Figure(data=data_scatter, layout=layout_scatter),\
           go.Figure(data=data_bar, layout=layout_bar),


if __name__ == '__main__':
    app.run_server(debug=True)








