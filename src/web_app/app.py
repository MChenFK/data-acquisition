import dash
from dash import dcc, html, Input, Output, State, dash_table
from dash.exceptions import PreventUpdate
from dash.dependencies import MATCH, ALL
import pandas as pd
import os
import plotly.graph_objs as go
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from constants import ITEMS

def get_data_path():
    try:
        with open("last_data_path.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Path file not found.")
        return None


FILE_NAME = get_data_path()
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CSV_PATH = os.path.abspath(os.path.join(ROOT_DIR, FILE_NAME))

SENSOR_COLUMNS = [
    "deposition rate (A/sec)",
    "power (%)",
    "pressure (Torr)",
    "temperature (C)",
    "crystal (kA)",
    "anode current (amp)",
    "neutralization current (amp)",
    "gas flow (sccm)"
]


MAX_POINTS = 5000  # limit points

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
    suppress_callback_exceptions=True,
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
        html.Button(
            "Pause",
            id="pause-button",
            n_clicks=0,
            style={
                'width': '100px',
                'minWidth': '100px',
                'maxWidth': '100px',
                'textAlign': 'center'
            }
        ),

        dcc.Store(id="pause-state", data=False),
    ], style={'textAlign': 'center', 'padding': '10px'}),

    html.Div([
        html.Div(
            dcc.Tabs(id='tabs', value='tab-all', children=[
                dcc.Tab(label='All Graphs', value='tab-all'),
                dcc.Tab(label='Single Graph', value='tab-single'),
                dcc.Tab(label='Overlay Graph', value='tab-overlay'),
                dcc.Tab(label='CSV Table', value='tab-table'),
            ]),
            style={'padding': '10px'},
            className='custom-tabs'
        ),
        
        dcc.Store(id='data-store'),
        dcc.Store(id='page-size-store', data=15),

        html.Div(id='tab-content'),
        dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0, disabled=False)
    ], id='main-content', style={'padding': '20px'})



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
                    value=SENSOR_COLUMNS,
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
            dcc.Graph(
                id='single-graph',
                figure=go.Figure(
                    layout=dict(
                        title='Loading...',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        margin=dict(l=30, r=10, t=40, b=30),
                    )
                ),
                style={'backgroundColor': 'transparent'}
            ),

            html.Div([
                html.Button("Previous", id='prev-graph', n_clicks=0),
                html.Button("Next", id='next-graph', n_clicks=0),
            ], style={'display': 'flex', 'gap': '10px', 'justifyContent': 'center', 'padding': '10px'})
        ])

    elif tab == 'tab-overlay':
        return html.Div([
            html.Div([
                html.Label("Select Graphs to Overlay:"),
                dcc.Checklist(
                    id='overlay-graph-selector',
                    options=[{'label': col, 'value': col} for col in SENSOR_COLUMNS],
                    value=["deposition rate (A/sec)", "temperature (C)"],  # defaults
                    labelStyle={'display': 'inline-block', 'marginRight': '15px'}
                )
            ], style={'padding': '10px'}),

            dcc.Graph(
                id='overlay-graph',
                style={'height': '500px', 'width': '100%'}
            )
        ])

    elif tab == 'tab-table':
        return html.Div([
            html.Button(
                "Download CSV",
                id="btn-download-csv",
                style={'margin': '10px 0'}
            ),
            dcc.Download(id="download-csv"),
            html.Label("Rows per page:"),
            dcc.Dropdown(
                id='page-size-selector',
                options=[{'label': str(n), 'value': n} for n in [10, 15, 25, 50, 100]],
                value=15,
                clearable=False,
                style={'width': '150px', 'margin': '10px 0'}
            ),
            dash_table.DataTable(
                id='csv-table',
                columns=[],
                data=[],
                page_size=15,
                style_table={
                    'overflowX': 'auto',
                    'backgroundColor': 'rgba(255, 255, 255, 0.3)',
                    'borderRadius': '5px',
                    'maxHeight': '500px',
                    'overflowY': 'auto',
                },
                style_header={
                    'backgroundColor': 'rgba(0, 51, 102, 0.7)',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'position': 'sticky',
                    'top': 0,
                    'zIndex': 1,
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '5px',
                    'backgroundColor': 'rgba(255, 255, 255, 0.2)',
                },
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
    return paused

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

    df = pd.DataFrame(data)

    csv_string = df.to_csv(index=False, encoding='utf-8')

    return dict(content=csv_string, filename=FILE_NAME)

def slice_for_plotting(df, max_plot_points=100):
    if len(df) > max_plot_points:
        return df.tail(max_plot_points)
    return df

def relayout_to_layout_update(relayout):
    layout_update = {}

    for k, v in relayout.items():
        if '.' in k:
            axis, detail = k.split('.', 1)
            if axis not in layout_update:
                layout_update[axis] = {}
            if detail.startswith("range["):
                idx = int(detail[len("range[")])
                layout_update[axis].setdefault("range", [None, None])[idx] = v
    return layout_update

@app.callback(
    Output('all-graphs-container', 'children'),
    Output('all-graphs-container', 'style'),
    Input('graph-selector', 'value'),
    Input('data-store', 'data'),
    Input('tabs', 'value'),
    State({'type': 'zoom-store', 'index': ALL}, 'data'),
    State({'type': 'zoom-store', 'index': ALL}, 'id'),
)
def update_all_graphs(selected_graphs, data, current_tab, all_zoom_data, all_zoom_ids):
    if current_tab != 'tab-all':
        raise dash.exceptions.PreventUpdate

    if not data:
        return html.Div("No data to display."), {}

    if not selected_graphs:
        return html.Div("No graphs selected."), {}

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    zoom_map = {zid['index']: zdata for zid, zdata in zip(all_zoom_ids, all_zoom_data)}

    ordered_selected = [col for col in SENSOR_COLUMNS if col in selected_graphs]
    graphs = []

    def relayout_to_layout_update(relayout):
        layout_update = {}
        for k, v in relayout.items():
            if '.' in k:
                axis, detail = k.split('.', 1)
                if axis not in layout_update:
                    layout_update[axis] = {}
                if detail.startswith("range["):
                    idx = int(detail[len("range[")])
                    layout_update[axis].setdefault("range", [None, None])[idx] = v
        return layout_update

    for col in ordered_selected:
        if col not in df.columns and col != "gas flow (sccm)":
            continue

        fig = go.Figure()

        if col == "gas flow (sccm)":
            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=df["AR flow (sccm)"],
                mode='lines+markers',
                name="AR"
            ))
            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=df["O2 flow (sccm)"],
                mode='lines+markers',
                name="O2",
                line=dict(dash='dot', color='green')
            ))
        else:
            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=df[col],
                mode='lines+markers',
                name=col
            ))


        fig.update_layout(
            title=col,
            margin=dict(l=30, r=10, t=40, b=30),
            paper_bgcolor='rgba(255,255,255,0.5)',
            plot_bgcolor='rgba(255,255,255,0)',
        )

        zoom_data = zoom_map.get(col)
        if zoom_data:
            fig.update_layout(relayout_to_layout_update(zoom_data))
        else:
            if len(df) > 100:
                fig.update_xaxes(range=[df['timestamp'].iloc[-100], df['timestamp'].iloc[-1]])

        graph = dcc.Graph(
            id={'type': 'sensor-graph', 'index': col},
            figure=fig,
            style={'height': '300px', 'width': '100%'},
            clear_on_unhover=False
        )

        zoom_store = dcc.Store(
            id={'type': 'zoom-store', 'index': col},
            data={}
        )

        graphs.append(html.Div([graph, zoom_store]))

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
    State({'type': 'sensor-graph', 'index': ALL}, 'id'),
    State('zoom-store', 'data'),
    prevent_initial_call=True
)
def update_zoom_store(all_relayout, all_ids, store_data):
    import json
    from dash.exceptions import PreventUpdate

    store_data = store_data or {}

    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    triggered_prop = ctx.triggered[0]['prop_id']
    triggered_id_str = triggered_prop.split('.')[0]
    try:
        triggered_id = json.loads(triggered_id_str)
        triggered_index = triggered_id['index']
    except (json.JSONDecodeError, KeyError):
        raise PreventUpdate

    # Match it against relayouts and ids
    for relayout, id_obj in zip(all_relayout, all_ids):
        if id_obj['index'] != triggered_index:
            continue

        if not relayout:
            break

        # Detect reset (autoscale)
        if relayout.get('xaxis.autorange') or relayout.get('yaxis.autorange'):
            store_data.pop(triggered_index, None)
            return store_data

        # Store zoom ranges
        keys_of_interest = ['xaxis.range[0]', 'xaxis.range[1]',
                            'yaxis.range[0]', 'yaxis.range[1]']
        zoom_data = {k: relayout[k] for k in keys_of_interest if k in relayout}
        if zoom_data:
            store_data[triggered_index] = zoom_data

        break

    return store_data

@app.callback(
    Output({'type': 'zoom-store', 'index': MATCH}, 'data'),
    Input({'type': 'sensor-graph', 'index': MATCH}, 'relayoutData'),
    State({'type': 'zoom-store', 'index': MATCH}, 'data'),
    prevent_initial_call=True
)
def update_individual_zoom(relayout, existing_zoom):
    if not relayout:
        raise dash.exceptions.PreventUpdate

    if relayout.get("xaxis.autorange") or relayout.get("yaxis.autorange"):
        return {}

    keys = ['xaxis.range[0]', 'xaxis.range[1]', 'yaxis.range[0]', 'yaxis.range[1]']
    return {k: relayout[k] for k in keys if k in relayout}

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
    State('single-graph', 'relayoutData'),
    prevent_initial_call=True
)
def update_single_graph(selected_col, data, relayout_data):
    if not data or selected_col is None:
        return go.Figure()
    df = pd.DataFrame(data)
    if selected_col not in df.columns and selected_col != "gas flow (sccm)":
        return go.Figure()

    fig = go.Figure()

    if selected_col == "gas flow (sccm)":
        fig.add_trace(go.Scatter(
            x=df["timestamp"],
            y=df["AR flow (sccm)"],
            mode='lines+markers',
            name="AR"
        ))
        fig.add_trace(go.Scatter(
            x=df["timestamp"],
            y=df["O2 flow (sccm)"],
            mode='lines+markers',
            name="O2",
            line=dict(dash='dot', color='green')
        ))
    else:
        fig.add_trace(go.Scatter(
            x=df["timestamp"],
            y=df[selected_col],
            mode='lines+markers',
            name=selected_col
        ))


    fig.update_layout(
        title=selected_col,
        margin=dict(l=30, r=10, t=40, b=30),
        paper_bgcolor='rgba(255,255,255,0.5)',
        plot_bgcolor='rgba(255,255,255,0)',
    )

    # Determine initial zoom range for last 100 points (if enough points)
    if len(df) > 100:
        start = df['timestamp'].iloc[-100]
        end = df['timestamp'].iloc[-1]
        
        if not relayout_data or 'xaxis.range[0]' not in relayout_data:
            fig.update_xaxes(range=[start, end])

    # Apply user zoom if exists
    if relayout_data:
        x_range = relayout_data.get("xaxis.range[0]"), relayout_data.get("xaxis.range[1]")
        y_range = relayout_data.get("yaxis.range[0]"), relayout_data.get("yaxis.range[1]")

        if all(x_range):
            fig.update_xaxes(range=x_range)
        if all(y_range):
            fig.update_yaxes(range=y_range)

    return fig

@app.callback(
    Output('overlay-graph', 'figure'),
    Input('overlay-graph-selector', 'value'),
    Input('data-store', 'data')
)
def update_overlay_graph(selected_columns, data):
    if not data or not selected_columns:
        fig = go.Figure()
        fig.update_layout(
            title="No data selected",
            paper_bgcolor='rgba(255,255,255,0.5)',
            plot_bgcolor='rgba(255,255,255,0)',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(l=30, r=10, t=40, b=30),
        )
        return fig


    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    fig = go.Figure()

    color_cycle = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
        "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
    ]

    for i, col in enumerate(selected_columns):
        if col not in df.columns and col != "gas flow (sccm)":
            continue

        if col == "gas flow (sccm)":
            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=df["AR flow (sccm)"],
                mode='lines+markers',
                name="AR",
                line=dict(color=color_cycle[i % len(color_cycle)])
            ))
            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=df["O2 flow (sccm)"],
                mode='lines+markers',
                name="O2",
                line=dict(dash='dot', color='green')
            ))
        else:
            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=df[col],
                mode='lines+markers',
                name=col,
                line=dict(color=color_cycle[i % len(color_cycle)])
            ))

    fig.update_layout(
        title="Overlay Graph",
        margin=dict(l=30, r=10, t=40, b=30),
        paper_bgcolor='rgba(255,255,255,0.5)',
        plot_bgcolor='rgba(255,255,255,0)',
        xaxis_title="Timestamp",
        yaxis_title="Sensor Values"
    )

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
