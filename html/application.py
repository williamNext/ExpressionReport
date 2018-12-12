

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
import plotly
from decimal import Decimal
from scripts.file_reader import *

app = dash.Dash(__name__)

# Boostrap CSS.
app.css.append_css({
    'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})

# noqa: E501
app.config['suppress_callback_exceptions'] = True
app.layout = html.Div(
    html.Div([
    ###################################################
    html.Div(
                [
                    html.H1(children='Expression Report',
                            style ={'margin-top' :'20px','margin-left' :'50px'}),

                ],className='twelve columns'

            ),

   ###########################################


    html.Div([

        ######## BANNER ########


        ################PARAGRAPHS################
        html.Div([
            html.P(children='Selecione o arquivo desejado arrastando ou clicando no botão '),
            html.P(
                'Obs: o arquivo selecionado deve ser o arquivo com final detailed.txt que é o Log detalhado das '
                'emoções analisadas no Facereader '
                'outros arquivos não seram lidos!', style={'margin-top': '20'})

        ], className='row', style={'margin-top': '50', 'margin-bottom': '50'}),

        ##################  UPLOAD FILE DRAG AND DROP ######################
        html.Div([

            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                }
                # Allow multiple files to be uploaded

            )

        ], className="row", style={'margin-top': '20'}),

        ################# File name #################
        html.H6(id='titulo', children='Graphname', style={'margin-top': '50', 'margin-bottom': '20'}),
        ################## DROPDOWN ##################
        html.Div([
            dcc.Dropdown(
                id='drop',
                options=[
                    {'label': 'Grafico temporal', 'value': 'linhas'},
                    {'label': 'Dominância das emoções', 'value': 'pie'},

                ],
                className='three columns',
                value="linhas",

            )
        ], className='row', id='dropdown', style={'visibility': 'hidden'}),
        ##################  RADIO BUTTONS DIV ###################

        html.Div(
            [

                html.Div(
                    [
                        html.P('  Escolha o tipo de Gráfico:'),
                        dcc.RadioItems(
                            id='radio_tipo',
                            options=[
                                {'label': 'Normal', 'value': 'normal'},
                                {'label': 'Log Scale', 'value': 'lscale'}
                            ],
                            value='normal',
                            labelStyle={'display': 'inline-block'}
                        )

                    ],
                    className='six columns',
                    style={'margin-top': '20'}
                ),

                html.Div(
                    [
                        html.P('  Escolha formato do tempo:'),
                        dcc.RadioItems(
                            id='radio_time',
                            options=[
                                {'label': 'Tempo Padrão', 'value': 'tp_padrao'},
                                {'label': 'Tempo Discretizado', 'value': 'tp_disc'}
                            ],
                            value='tp_disc',
                            labelStyle={'display': 'inline-block'}
                        )

                    ],
                    className='six columns',
                    style={'margin-top': '20'}
                ),

            ], className="row", id='btn', style={'margin-top': '20', 'visibility': 'hidden'}
        ),

        ########### LINE CHART DIV #######################
        html.Div(
            [

                html.Div([
                    dcc.Graph(
                        id='example-graph'
                    )
                ], className='twelve columns'
                ),

            ], className="row", id='graph', style={'visibility': 'hidden', 'margin-right': '300'}
        ),

        html.P(id='placeholder')
    ], className='eleven columns', style={'margin-left': '50'}),
    ])
)



### UPDATE CHART CALLBACK
@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('radio_tipo', 'value'), dash.dependencies.Input('radio_time', 'value'),
     dash.dependencies.Input('upload-data', 'filename'), dash.dependencies.Input('drop', 'value')])
def update_img(selector_chart, selector_time, filename, value):
    if 'linhas' in value:
        if 'lscale' in selector_chart:
            if 'tp_padrao' in selector_time:
                figure = {
                    'data': create_data_figure(videoTime),
                    'layout': go.Layout(
                        autosize=False,

                        height=550,
                        yaxis={'type': 'log', 'title': 'Values'},
                        xaxis=dict(
                            rangeselector=dict(

                            ),
                            rangeslider=dict(thickness='0.10'),

                        ),

                        legend=dict(orientation="v"),

                    )

                }
            if 'tp_disc' in selector_time:
                figure = {
                    'data': create_data_figure(countlist),
                    'layout': go.Layout(
                        autosize=False,

                        height=550,
                        yaxis={'type': 'log', 'title': 'Values'},
                        xaxis=dict(
                            rangeselector=dict(

                            ),
                            rangeslider=dict(thickness='0.10'),

                        ),

                        legend=dict(orientation="v")
                    )

                }

        if 'normal' in selector_chart:
            if 'tp_padrao' in selector_time:
                figure = {
                    'data': create_data_figure(videoTime),
                    'layout': go.Layout(
                        autosize=False,

                        height=550,
                        yaxis={'title': 'Values'},
                        xaxis=dict(
                            rangeselector=dict(

                            ),
                            rangeslider=dict(thickness='0.10'),

                        ),
                        legend=dict(orientation="v")

                    )

                }
            if 'tp_disc' in selector_time:
                figure = {
                    'data': create_data_figure(countlist),
                    'layout': go.Layout(
                        autosize=False,

                        height=550,
                        yaxis={'title': 'Values'},
                        xaxis=dict(
                            rangeselector=dict(

                            ),
                            rangeslider=dict(thickness='0.10'),

                        ),

                        legend=dict(orientation="v"),

                    )

                }
    if 'pie' in value:
        trace = go.Pie(labels=['neutral', 'Happy', 'Sad', 'Angry', 'Suprised', 'Scared', 'Disgusted'],
                       values=make_pie_data())

        figure = {'data': [trace]}

    return figure


@app.callback(
    dash.dependencies.Output('placeholder', 'children'),
    [dash.dependencies.Input('upload-data', 'contents'),
     dash.dependencies.Input('upload-data', 'filename')])
def load_arquives(contents, filename):
    if filename is not None:
        rest, conteudo = contents.split(',')
        read_file(conteudo)
''


@app.callback(
    dash.dependencies.Output('titulo', 'children'),
    [dash.dependencies.Input('upload-data', 'filename')])
def changeName(filename):
    name = str(filename)
    if name.endswith('.txt'):
        name.replace('.txt', '')

        return 'Nome do arquivo: ' + name


@app.callback(
    dash.dependencies.Output('btn', 'style'),
    [dash.dependencies.Input('upload-data', 'filename'), dash.dependencies.Input('drop', 'value')])
def visibilidade_btn(filename, values):
    if filename is not None:
        if 'pie' in values:
            return {'visbility': 'hidden', 'display': 'none'}
        if 'linhas' in values:
            return {'visbility': 'visible', 'display': 'block'}

    return {'visbility': 'hidden', 'display': 'none'}


@app.callback(
    dash.dependencies.Output('graph', 'style'),
    [dash.dependencies.Input('upload-data', 'filename')])
def visibilidade_graph(filename):
    if filename is not None:
        return {'visibility': 'visible'}

    return {'visibility': 'hidden'}


@app.callback(
    dash.dependencies.Output('dropdown', 'style'),
    [dash.dependencies.Input('upload-data', 'filename')])
def visibilidade_drop(filename):
    if filename is not None:
        return {'visibility': 'visible'}

    return {'visibility': 'hidden'}


if __name__ == '__main__':
    app.run_server(debug=True)
