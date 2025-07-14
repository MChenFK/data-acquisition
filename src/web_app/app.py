import dash
from dash import dcc, html, Input, Output, State, dash_table
from dash.dependencies import MATCH, ALL
import pandas as pd
import os
import plotly.graph_objs as go
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from constants import ITEMS

FILE_NAME = "data.csv"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Constants and data
CSV_PATH = os.path.abspath(os.path.join(ROOT_DIR, 'data', FILE_NAME))
SENSOR_COLUMNS = ITEMS

MAX_POINTS = 100  # limit points to plot

def read_csv():
    if not os.path.exists(CSV_PATH):
        return None
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()
    if 'timestamp' not in df.columns:
        return None
    return df.tail(MAX_POINTS)

app = dash.Dash(
    __name__,
    assets_folder=os.path.join(ROOT_DIR, 'src', 'web_app', 'assets')
)
server = app.server
app.title = "40 Inch Data"

app.layout = html.Div([
    # Banner
    html.Div([
        html.H1("Welcome to the 40 Inch Beach", style={'textAlign': 'center', 'padding': '10px'}),
    ]),

    html.Div([
        html.Button("Pause", id="pause-button", n_clicks=0),
        dcc.Store(id="pause-state", data=False),
    ], style={'textAlign': 'center', 'padding': '10px'}),

    html.Div([
        dcc.Tabs(id='tabs', value='tab-all', children=[
            dcc.Tab(label='All Graphs', value='tab-all'),
            dcc.Tab(label='Single Graph View', value='tab-single'),
            dcc.Tab(label='CSV Table', value='tab-table'),
        ], className='custom-tabs',),
        
        dcc.Store(id='data-store'),
        dcc.Store(id='page-size-store', data=15),
        html.Div(id='tab-content'),
        dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0, disabled=False)
    ], id='main-content', style={'padding': '20px'}),


])

# Callback to update data-store every interval
@app.callback(
    Output('data-store', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_data(n):
    df = read_csv()
    if df is None:
        return {}
    return df.to_dict('records')

# Callback to render tab content
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value'),
    State('data-store', 'data')
)
def render_tab(tab, data):
    if not data:
        df = read_csv()
        if df is None:
            return html.Div("No data available.")
        data = df.to_dict('records')
    
    df = pd.DataFrame(data)

    if tab == 'tab-all':
        # All graphs tab content
        return html.Div([
            html.Div([
                html.Label("Select Graphs to Show:"),
                dcc.Checklist(
                    id='graph-selector',
                    options=[{'label': col, 'value': col} for col in SENSOR_COLUMNS],
                    value=SENSOR_COLUMNS,  # default all selected
                    labelStyle={'display': 'inline-block', 'marginRight': '15px'}
                )
            ], style={'padding': '10px'}),
            html.Div(id='all-graphs-container', style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(350px, 1fr))',
                'gap': '15px',
                'padding': '10px'
            }),
        ])

    elif tab == 'tab-single':
        # Single graph view content
        return html.Div([
            dcc.Dropdown(
                id='single-graph-dropdown',
                options=[{'label': col, 'value': col} for col in SENSOR_COLUMNS],
                value=SENSOR_COLUMNS[0],
                clearable=False,
                style={'width': '300px', 'margin': '10px 0'}
            ),
            dcc.Graph(id='single-graph'),
            html.Div([
                html.Button("Previous", id='prev-graph', n_clicks=0),
                html.Button("Next", id='next-graph', n_clicks=0),
            ], style={'display': 'flex', 'gap': '10px', 'justifyContent': 'center', 'padding': '10px'})
        ])

    elif tab == 'tab-table':
        return html.Div([
            html.Button("Download CSV", id="btn-download-csv"),
            dcc.Download(id="download-csv"),
            html.Label("Rows per page:"),
            dcc.Dropdown(
                id='page-size-selector',
                options=[{'label': str(n), 'value': n} for n in [10, 15, 25, 50, 100]],
                value=15,
                clearable=False,
                style={'width': '150px'}
            ),
            dash_table.DataTable(
                id='csv-table',
                columns=[],
                data=[],
                page_size=15,
                style_table={'overflowX': 'auto'},
                style_header={'backgroundColor': '#003366', 'color': 'white', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'left', 'padding': '5px'},
            )
        ])

@app.callback(
    Output("pause-state", "data"),
    Input("pause-button", "n_clicks"),
    State("pause-state", "data")
)
def toggle_pause(n_clicks, paused):
    if n_clicks == 0:
        return paused
    return not paused

@app.callback(
    Output("interval-component", "disabled"),
    Input("pause-state", "data")
)
def control_interval(paused):
    return paused  # True disables interval

@app.callback(
    Output("pause-button", "children"),
    Input("pause-state", "data")
)
def update_pause_button(paused):
    return "Resume" if paused else "Pause"


@app.callback(
    Output("download-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    State('data-store', 'data'),
    prevent_initial_call=True,
)
def generate_csv(n_clicks, data):
    if not data:
        return dash.no_update

    # Convert data (list of dicts) back to DataFrame
    df = pd.DataFrame(data)

    # Use io.StringIO to create in-memory CSV string
    csv_string = df.to_csv(index=False, encoding='utf-8')

    return dict(content=csv_string, filename=FILE_NAME)

@app.callback(
    [Output('all-graphs-container', 'children'),
     Output('all-graphs-container', 'style')],
    [Input('graph-selector', 'value'),
     Input('data-store', 'data'),
     Input('tabs', 'value')]
)
def update_all_graphs(selected_graphs, data, current_tab):
    if current_tab != 'tab-all':
        raise dash.exceptions.PreventUpdate

    if not data:
        return html.Div("No data to display."), {}
    if not selected_graphs:
        return html.Div("No graphs selected."), {}

    df = pd.DataFrame(data)
    ordered_selected = [col for col in SENSOR_COLUMNS if col in selected_graphs]

    graphs = []
    for col in ordered_selected:
        if col not in df.columns:
            continue
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df[col],
            mode='lines+markers',
            name=col
        ))
        fig.update_layout(title=col, margin=dict(l=30, r=10, t=40, b=30))

        graphs.append(
            dcc.Graph(
                id={'type': 'sensor-graph', 'index': col},
                figure=fig,
                style={'height': '300px', 'width': '100%'},
                clear_on_unhover=False
            )
        )



    num_graphs = len(graphs) or 1

    container_style = {
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(350px, 1fr))',
        'gap': '15px',
        'padding': '10px',
        'width': '100%',
        'boxSizing': 'border-box',
    }

    return graphs, container_style

@app.callback(
    Output('zoom-store', 'data'),
    Input({'type': 'sensor-graph', 'index': ALL}, 'relayoutData'),
    State('zoom-store', 'data'),
    prevent_initial_call=True
)
def update_zoom_store(all_relayout, store_data):
    store_data = store_data or {}
    for i, r in enumerate(all_relayout):
        if r and 'xaxis.range[0]' in r:
            col = SENSOR_COLUMNS[i]
            store_data[col] = r
    return store_data

# Single graph callbacks (dropdown + next/prev buttons)
@app.callback(
    Output('single-graph-dropdown', 'value'),
    [Input('prev-graph', 'n_clicks'), Input('next-graph', 'n_clicks')],
    State('single-graph-dropdown', 'value')
)
def cycle_single_graph(prev_clicks, next_clicks, current):
    if current is None:
        return SENSOR_COLUMNS[0]

    ctx = dash.callback_context
    if not ctx.triggered:
        return current
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    current_index = SENSOR_COLUMNS.index(current)

    if button_id == 'prev-graph':
        new_index = (current_index - 1) % len(SENSOR_COLUMNS)
    elif button_id == 'next-graph':
        new_index = (current_index + 1) % len(SENSOR_COLUMNS)
    else:
        new_index = current_index

    return SENSOR_COLUMNS[new_index]

@app.callback(
    Output('single-graph', 'figure'),
    [Input('single-graph-dropdown', 'value'),
     Input('data-store', 'data')],
    State('single-graph', 'relayoutData')
)
def update_single_graph(selected_col, data, relayout_data):
    if not data or selected_col is None:
        return go.Figure()
    df = pd.DataFrame(data)
    if selected_col not in df.columns:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df[selected_col],
        mode='lines+markers',
        name=selected_col
    ))
    fig.update_layout(title=selected_col, margin=dict(l=30, r=10, t=40, b=30))

    if relayout_data:
        x_range = relayout_data.get("xaxis.range[0]"), relayout_data.get("xaxis.range[1]")
        y_range = relayout_data.get("yaxis.range[0]"), relayout_data.get("yaxis.range[1]")

        if all(x_range):
            fig.update_xaxes(range=x_range)
        if all(y_range):
            fig.update_yaxes(range=y_range)

    return fig


@app.callback(
    Output('page-size-store', 'data'),
    Input('page-size-selector', 'value')
)
def update_page_size(selected):
    return selected

@app.callback(
    [Output('csv-table', 'data'),
     Output('csv-table', 'columns'),
     Output('csv-table', 'page_size')],
    [Input('data-store', 'data'),
     Input('tabs', 'value'),
     Input('page-size-store', 'data')]
)
def update_csv_table(data, current_tab, page_size):
    if current_tab != 'tab-table' or not data:
        raise dash.exceptions.PreventUpdate
    df = pd.DataFrame(data)
    columns = [{"name": i, "id": i} for i in df.columns]
    return df.to_dict('records'), columns, page_size

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)
