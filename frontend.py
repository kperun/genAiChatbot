from dash import Dash, dcc, html, callback, State, Output, Input, dash_table
from requests import post

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1('Sample Frontend via Dash', style={'color': '#ff22ff'}),
        html.Br(),
        html.H3('Input:'),
        dcc.Textarea(id='input-textarea', value='', placeholder='Type here...',
                     style={'width': '90%', 'height': '100px'}),
        html.Br(),
        html.Button('Submit', id='input-submit', n_clicks=0),
        html.H3('Output:'),
        html.Div(id='output-response', style={'background-color': 'gray', 'disabled': True}),
        html.Br(),
        html.H3('History:'),
        html.Div(id='history-box', style={'background-color': 'gray'})
    ]
)

history = []


@callback([
    Output('input-textarea', 'value'),
    Output('output-response', 'children'),
    Output('history-box', 'children')],
    Input('input-submit', 'n_clicks'),
    State('input-textarea', 'value'))
def update_output(n_clicks, value):
    if n_clicks > 0:
        result = post(url='http://localhost:8000/prompt', json={'request': value})
        file = None
        page = None
        if result.status_code == 200:
            response = result.json()['response']
            file = result.json()['file']
            page = result.json()['page']
        else:
            response = f'Error: {result.status_code}'
        textarea = ''
        message = html.Div([
            html.Div('Question: ' + value),
            html.Br(),
            html.Div('Answer: ' + response),
            html.Div('Source:' + file + ', page ' + page) if file is not None else None
        ])
        history.append({'question': value, 'answer': response, 'source': file, 'page': page})
        history_box = dash_table.DataTable(history)
        return textarea, message, history_box
    else:
        return None, None, None


if __name__ == '__main__':
    app.run(debug=True, port=5000)
