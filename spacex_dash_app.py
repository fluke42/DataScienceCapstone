# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
site_list = spacex_df['Launch Site']
site_list = site_list.drop_duplicates(keep='first', inplace=False)
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[{'label': 'All Sites','value':'ALL'},
                                    {'label':i, 'value': i} for i in site_list],
                                        value='ALL'
                                        placeholder='Select a Launch Site Here'

    ),
])
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider' min=0, max=10000,step=1000,value=[min_payload, max_payload])

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value'))

def piechart(site_dropdown):
    if site_dropdown == 'ALL':
        title_pie = f'Successful Launches for Site {site_dropdown}'
        fig = px.pie(spacex_df, values=['class'], names = ['Launch Site'], title=title_pie)
        return fig
    else:
        filtered_drop = spacex_df[spacex_df['Launch Site']==-site_dropdown]
        filtered_launch = filtered_drop.groupby(['Launch Site','class']).size().reset_index(name='class count')
        title_pie = f'Successful Launches for Site {site_dropdown}'
        fig = px.pie(filtered_launch, values='class count', names='class', title=title_pie)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property='figure'), [Input(component_id='site-dropdown', component_property='value'),
Input(component_id = 'payload-slider',component_property='value')])

def build_scatter(slider_range, site_dropdown):
    low, high = slider_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    filtered_df = mask[mask['Launch Site'] == 'site']
    
    if site-dropdown == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Payload vs Outcome for All Sites')
        return fig
    else:
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Payload vs Outcome for '+site)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
