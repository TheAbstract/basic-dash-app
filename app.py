import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from flask import Flask
import pandas as pd

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Data prep
df = pd.read_csv('matric-pass-rate.csv')
dff = df.columns
Provinces = dff[1:]

# Dont need this
markdown_text = """ """

app.layout = html.Div([
	html.Div([
    # Interactive dropdown
		html.Div([
			dcc.Dropdown(
				id='yaxis',
				options=[{'label':i,'value':i} for i in Provinces],
				value='province-by-year'
			)
		], style={'width': '40%'})
	]),

	html.Div([dcc.Graph(id='scatter-by-year', #'scatter-by-year'
		figure={
			'data': [go.Scatter(
				x=df['Province'],
				y=[0,0],
				# mode='markers'
			)],
			'layout': go.Layout(
				title = 'Use the dropdown to display the chart ...',
				xaxis={'tickformat': 'd'}
			)
		}
		)
	], style={'width':'50%', 'display':'inline-block'}),

	html.Div([dcc.Graph( id='bar-by-province', #'bar-by-province'
		figure={
			'data': [go.Bar(
				x=df['Province'],
				y=df['2009'],
				name='2009'
				),
				go.Bar(
                                x=df['Province'],
                                y=df['2010'],
                                name='2010'
                                ),
				go.Bar(
                                x=df['Province'],
                                y=df['2011'],
                                name='2011'
                                ),
				go.Bar(
                                x=df['Province'],
                                y=df['2012'],
                                name='2012'
                                ),
				go.Bar(
                                x=df['Province'],
                                y=df['2013'],
                                name='2013'
                                )
			],
			'layout': go.Layout(
				title ='Matric pass rate (2009-2013',
                yaxis={'title': 'Pass rate (%)'}
				# barmode='stack'
			)
		}
		)
	], style={'width':'50%', 'display':'inline-block'}),

	html.Div([dcc.Graph( id='boxplot', #'boxplot'
		figure={
			'data': [go.Box(
			y=df['2010'],
			name='2010'
			),
			go.Box(
                        y=df['2011'],
                        name='2011'
                        ),
			go.Box(
                        y=df['2012'],
                        name='2012'
                        ),
			go.Box(
                        y=df['2013'],
                        name='2013'
                        ),
			],
			'layout': go.Layout(
			title=''
			)
		}
	)
	], style={'width':'50%', 'display':'inline-block'}),

	html.Div([
		dcc.Markdown(children=markdown_text)
	])
	], style={'padding':10})

#Here is the callback
@app.callback(
	Output('scatter-by-year', 'figure'),
	[Input ('yaxis', 'value')])
def update_graphic(yaxis_rate):
	return {
		'data': [go.Scatter(
			x=df['Province'],
			y=df[yaxis_rate],
			mode='lines+markers',
			marker={
				'size': 15,
				'opacity': 0.5,
				'line': {'width':0.5, 'color':'white'}
			}
		)],
		'layout': go.Layout(
			title='{} '.format(yaxis_rate),
			xaxis={'title': 'Province'},
			yaxis={'title': yaxis_rate},
			hovermode='closest'
		)
	}

if __name__ == '__main__':
	app.run_server(debug=True)
