import numpy as np
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

start_amplitude = 1.0
start_freq = 1.0
start_phase = 0.0
start_noise_mean = 0.0
start_noise_std = 0.1
start_window = 10

time = np.linspace(0, 2 * np.pi, 1000)
sampling_rate = 1.0 / (time[1] - time[0])


noise = np.random.normal(start_noise_mean, start_noise_std, size=time.shape)

def ma_filter(harmonic, window_size):
    window_size = int(window_size)
    kernel = np.ones(window_size) / window_size
    filtered = np.convolve(harmonic, kernel, mode='same')
    return filtered


app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.H1("2 Частина", style={"textAlign": "center", "color": "black", "margin": "0px"}),

        html.Label("Amplitude (А) :"),
        dcc.Slider(id='amplitude', min=0, max=10, step=0.1, marks={0:'0',5:'5',10:'10'}, value=start_amplitude, tooltip={
            "always_visible": False, "placement": "bottom"}),

        html.Label("Frequency (f):"),
        dcc.Slider(id='frequency', min=0.1, max=10, step=0.1, marks={0.1:'0.1',5:'5',10:'10'}, value=start_freq, tooltip={
            "always_visible": False, "placement": "bottom"}),

        html.Label("Phase (φ):"),
        dcc.Slider(id='phase', min=0, max=2*np.pi, step=0.1, marks={0:'0',3.14:'π',6.28:'2π'}, value=start_phase, tooltip={
            "always_visible": False, "placement": "bottom"}),

        html.Label("Noise Mean:"),
        dcc.Slider(id='noise-mean', min=-1, max=1, step=0.05, marks={-1:'-1',0:'0',1:'1'}, value=start_noise_mean, tooltip={
            "always_visible": False, "placement": "bottom"}),

        html.Label("Noise Std:"),
        dcc.Slider(id='noise-std', min=0, max=1.0, step=0.05, marks={0:'0',0.5:'0.5',1:'1'}, value=start_noise_std, tooltip={
            "always_visible": False, "placement": "bottom"}),

        html.Label("Show Noise:"),
        dcc.Checklist(id='show-noise', options=[{'label':'Так','value':'show'}], value=['show'], inline=True),

        html.Label("Filter window size:"),
        dcc.Slider(id='filter-window', min=1, max=50, step=1,
                    marks={1:'1', 10:'10', 20:'20', 30:'30', 40:'40', 50:'50'},
                    value=start_window, tooltip={"always_visible": False, "placement": "bottom"}),

        html.Label("Filter:"),
        dcc.Dropdown(id='filter-type',
                    options=[{'label': 'Moving Average', 'value': 'MovingAvarage'}],
                    value='MovingAvarage', clearable=False),

        html.Button('Reset', id='reset-btn', n_clicks=0, style={
                        'width': '100%', 'padding': '5px', 'backgroundColor': '#0074D9', 'color': 'white',
                        'border': 'none', 'borderRadius': '4px','cursor': 'pointer', 'fontSize': '16px', 'margin-top':'15px'
                    })
    ], style={'width':'70%', 'margin':'auto', 'padding':'20px', 'padding-bottom':'0px'}),

    html.Div([
        dcc.Graph(id='raw-graph', style={'width':'48%', 'display':'inline-block', 'height': '40vh'}),
        dcc.Graph(id='filtered-graph', style={'width':'48%', 'display':'inline-block', 'height': '40vh'})
    ], style={'padding-top':'0px'})

])

@app.callback(
    [Output('amplitude','value'),
     Output('frequency','value'),
     Output('phase','value'),
     Output('noise-mean','value'),
     Output('noise-std','value'),
     Output('show-noise','value'),
     Output('filter-type','value'),
     Output('filter-window','value')],
    [Input('reset-btn','n_clicks')]
)

def reset_controls(n_clicks):
    if n_clicks > 0:
        return start_amplitude, start_freq, start_phase, start_noise_mean, start_noise_std, ['show'], 'MovingAvarage', start_window
    raise dash.exceptions.PreventUpdate


@app.callback(
    [Output('raw-graph','figure'),
     Output('filtered-graph','figure')],
    [Input('amplitude','value'),
     Input('frequency','value'),
     Input('phase','value'),
     Input('noise-mean','value'),
     Input('noise-std','value'),
     Input('show-noise','value'),
     Input('filter-type','value'),
     Input('filter-window','value'),
     Input('reset-btn','n_clicks')]
)

def update_graphs(amplitude, frequency, phase, noise_mean, noise_std, show_noise_list, filter_type, window, n_clicks):

    show_noise = 'show' in show_noise_list
    global noise

    callback_context_ = dash.callback_context
    triggered = callback_context_.triggered[0]['prop_id'].split('.')[0]
    if triggered in ['reset-btn','noise-mean','noise-std']:
        noise = np.random.normal(noise_mean, noise_std, size=time.shape)

    harmonic = amplitude * np.sin(2 * np.pi * frequency * time + phase)
    if show_noise:
        raw = harmonic + noise
    else:
        raw = harmonic

    if filter_type == 'MovingAvarage':
        filtered = ma_filter(raw, window)
    else:
        filtered = raw


    raw_fig = go.Figure(data=[go.Scatter(x=time, y=raw, mode='lines', line=dict(color='#6bbb11'))])
    filtered_fig = go.Figure(data=[go.Scatter(x=time, y=filtered, mode='lines', line=dict(color='orange'))])
    raw_fig.update_layout(title='Harmonic', xaxis_title='Time (t)', yaxis_title='Amplitude (А)', template='plotly_white')
    filtered_fig.update_layout(title='Harmonic after filtering', xaxis_title='Time (t)', yaxis_title='Amplitude (А)', template='plotly_white')

    return raw_fig, filtered_fig

if __name__ == '__main__':
    app.run(debug=True)
