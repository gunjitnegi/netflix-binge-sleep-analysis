# dashboard_updated.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
import threading
import time
import os

# -----------------------------
# Step 1: Load feature-engineered data
# -----------------------------
df = pd.read_csv('data/processed/netflix_sleep_features.csv')

# Convert datetime columns
df['Sleep Start Time'] = pd.to_datetime(df['Sleep Start Time'])
df['Sleep End Time'] = pd.to_datetime(df['Sleep End Time'])
df['Last Episode End Time'] = pd.to_datetime(df['Last Episode End Time'])

# -----------------------------
# Step 2: Descriptive statistics
# -----------------------------
avg_sleep_binge = df[df['Night_Binge']]['Total Sleep Duration (hrs)'].mean()
avg_sleep_non_binge = df[~df['Night_Binge']]['Total Sleep Duration (hrs)'].mean()
corr_matrix = df[['Total Sleep Duration (hrs)', 'Total Viewing Time (hrs)', 'Sleep_Score']].corr()

# -----------------------------
# Step 3: Scatter plot (interactive)
# -----------------------------
scatter_fig = px.scatter(
    df,
    x='Total Viewing Time (hrs)',
    y='Total Sleep Duration (hrs)',
    color='Late_Night_Viewing',
    symbol='Is_Weekend',
    hover_data=['Sleep_Score', 'Night_Binge', 'Viewing_Category'],
    title="Netflix Duration vs Sleep Hours",
    color_discrete_map={True:'red', False:'blue'},
)
scatter_fig.update_traces(marker=dict(size=12, opacity=0.7), selector=dict(mode='markers'))
scatter_fig.update_layout(hovermode='closest')

# -----------------------------
# Step 4: Pie chart of Viewing Categories
# -----------------------------
pie_fig = px.pie(
    df,
    names='Viewing_Category',
    title="Distribution of Viewing Duration Categories",
    color='Viewing_Category',
    color_discrete_map={'Short':'#FFA07A', 'Medium':'#20B2AA', 'Long':'#9370DB'}
)

# -----------------------------
# Step 5: Time series: Sleep duration & viewing time (more detailed)
# -----------------------------
df_sorted = df.sort_values('Sleep Start Time')
time_series_fig = go.Figure()
time_series_fig.add_trace(go.Scatter(
    x=df_sorted['Sleep Start Time'],
    y=df_sorted['Total Sleep Duration (hrs)'],
    mode='lines+markers',
    name='Sleep Duration',
    line=dict(color='blue'),
    marker=dict(size=6),
    hovertemplate='Date: %{x}<br>Sleep Duration: %{y} hrs<extra></extra>'
))
time_series_fig.add_trace(go.Scatter(
    x=df_sorted['Sleep Start Time'],
    y=df_sorted['Total Viewing Time (hrs)'],
    mode='lines+markers',
    name='Viewing Duration',
    line=dict(color='orange'),
    marker=dict(size=6),
    hovertemplate='Date: %{x}<br>Viewing Time: %{y} hrs<extra></extra>'
))
time_series_fig.update_layout(
    title="Sleep & Netflix Viewing Trends Over Time",
    xaxis_title="Date",
    yaxis_title="Hours",
    legend=dict(x=0.02, y=0.98)
)

# -----------------------------
# Step 6: Dash App Layout
# -----------------------------
app = Dash(__name__)
app.layout = html.Div(style={'backgroundColor':'#f9f9f9','padding':'10px'}, children=[
    html.H1("Netflix Binge & Sleep Analysis Dashboard", style={'textAlign':'center', 'color':'#333'}),
    
    html.Div([
        html.H3(f"Average Sleep Duration on Binge Days: {avg_sleep_binge:.2f} hrs"),
        html.H3(f"Average Sleep Duration on Non-Binge Days: {avg_sleep_non_binge:.2f} hrs")
    ], style={'textAlign':'center', 'margin':'20px'}),
    
    html.Div([
        dcc.Graph(figure=scatter_fig)
    ]),
    
    html.Div([
        dcc.Graph(figure=pie_fig)
    ], style={'marginTop':'30px'}),
    
    html.Div([
        dcc.Graph(figure=time_series_fig)
    ], style={'marginTop':'30px'}),
    
    html.Div([
        html.H3("Correlation Matrix"),
        dcc.Graph(
            figure=px.imshow(
                corr_matrix,
                text_auto=True,
                color_continuous_scale='Plasma',
                title="Correlation Coefficients"
            )
        )
    ], style={'marginTop':'30px'})
])

# -----------------------------
# Step 7: Run Dash App
# -----------------------------
def run_dash():
    app.run_server(debug=True)
if __name__ == '__main__':
    dash_thread = threading.Thread(target=run_dash)
    dash_thread.start()

    # Automatically stop the server after 30 minutes (1800 seconds)
    time.sleep(1800)
    print("Closing Dash server automatically...")
    os._exit(0)