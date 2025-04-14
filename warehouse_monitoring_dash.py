import random
from datetime import datetime, timedelta
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Initialize Dash app
app = Dash(__name__)
app.title = "Warehouse Monitoring Dashboard"
server = app.server  # Required for Render deployment

# Generate initial data
def generate_data(n=500):
    now = datetime.now()
    status = [random.choice(['success']*9 + ['failure']) for _ in range(n)]
    return pd.DataFrame({
        "timestamp": [now - timedelta(minutes=random.randint(0, 1440)) for _ in range(n)],
        "machine_id": [f"M-{random.randint(1, 5)}" for _ in range(n)],
        "task_duration": [round(random.uniform(5.0, 60.0), 2) for _ in range(n)],
        "status": status,
        "error_code": [
            random.choice(["E-100", "E-200", "E-300"] if s == "failure" else "None")
            for s in status
        ]
    })

df = generate_data(1000)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Layout
app.layout = html.Div([
    html.H1("Warehouse Monitoring Dashboard"),
    
    dcc.DatePickerRange(
        id="date-range",
        min_date_allowed=df["timestamp"].min(),
        max_date_allowed=df["timestamp"].max(),
        start_date=df["timestamp"].min(),
        end_date=df["timestamp"].max()
    ),
    
    dcc.Dropdown(
        id="machine-dropdown",
        options=[{"label": m, "value": m} for m in df["machine_id"].unique()],
        placeholder="Select Machine"
    ),
    
    dcc.Graph(id="incident-graph"),
    dcc.Graph(id="duration-graph"),
    
    dash_table.DataTable(
        id="log-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10
    )
])

# Callbacks
@app.callback(
    [Output("incident-graph", "figure"),
     Output("duration-graph", "figure"),
     Output("log-table", "data")],
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("machine-dropdown", "value")]
)
def update_dashboard(start_date, end_date, machine_id):
    filtered_df = df.copy()
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df["timestamp"] >= pd.to_datetime(start_date)) &
            (filtered_df["timestamp"] <= pd.to_datetime(end_date))
        ]
    if machine_id:
        filtered_df = filtered_df[filtered_df["machine_id"] == machine_id]
    
    fig1 = px.histogram(
        filtered_df[filtered_df["status"] == "failure"], 
        x="error_code", 
        title="Error Distribution"
    )
    
    fig2 = px.scatter(
        filtered_df, 
        x="timestamp", 
        y="task_duration", 
        color="machine_id",
        title="Task Duration by Machine"
    )
    
    return fig1, fig2, filtered_df.to_dict("records")

if __name__ == '__main__':
    app.run(debug=True)
