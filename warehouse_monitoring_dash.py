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

# ---------------------- Data Simulation ----------------------
def generate_data(n=500):
    now = datetime.now()
    data = {
        "timestamp": [],
        "machine_id": [],
        "task_duration": [],
        "status": [],
        "error_code": []
    }
    
    for _ in range(n):
        timestamp = now - timedelta(minutes=random.randint(0, 1440))
        machine_id = f"M-{random.randint(1, 5)}"
        task_duration = round(random.uniform(5.0, 60.0), 2)
        status = random.choice(["success"] * 9 + ["failure"])
        error_code = random.choice(["E-100", "E-200", "E-300"] if status == "failure" else ["None"])
        
        data["timestamp"].append(timestamp)
        data["machine_id"].append(machine_id)
        data["task_duration"].append(task_duration)
        data["status"].append(status)
        data["error_code"].append(error_code)
    
    return pd.DataFrame(data)

# Generate initial data
df = generate_data(1000)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ---------------------- Dashboard Layout ----------------------
app.layout = html.Div([
    html.H1("Warehouse Monitoring Dashboard", style={"textAlign": "center"}),
    
    html.Div([
        dcc.DatePickerRange(
            id="date-range",
            min_date_allowed=df["timestamp"].min(),
            max_date_allowed=df["timestamp"].max(),
            start_date=df["timestamp"].min(),
            end_date=df["timestamp"].max(),
            display_format='YYYY-MM-DD'
        ),
        
        dcc.Dropdown(
            id="machine-dropdown",
            options=[{"label": m, "value": m} for m in df["machine_id"].unique()],
            value=None,
            placeholder="Select Machine (Optional)",
            clearable=True,
            style={"width": "50%", "marginTop": "10px"}
        ),
    ], style={"padding": "20px", "backgroundColor": "#f9f9f9"}),
    
    dcc.Graph(id="incident-graph"),
    dcc.Graph(id="duration-graph"),
    
    html.H3("Log Records", style={"marginTop": "30px"}),
    dash_table.DataTable(
        id="log-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={
            'minWidth': '100px', 'width': '150px', 'maxWidth': '180px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        }
    )
])

# ---------------------- Callbacks ----------------------
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
    
    # Apply date filter
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df["timestamp"] >= pd.to_datetime(start_date)) &
            (filtered_df["timestamp"] <= pd.to_datetime(end_date))
        ]
    
    # Apply machine filter
    if machine_id:
        filtered_df = filtered_df[filtered_df["machine_id"] == machine_id]
    
    # Create graphs
    err_df = filtered_df[filtered_df["status"] == "failure"]
    fig1 = px.histogram(
        err_df, 
        x="error_code", 
        title="Incident Frequency by Error Code",
        color="error_code"
    )
    
    fig2 = px.scatter(
        filtered_df, 
        x="timestamp", 
        y="task_duration", 
        color="machine_id",
        title="Task Duration Over Time"
    )
    
    return fig1, fig2, filtered_df.to_dict("records")

# ---------------------- Run App ----------------------
if __name__ == '__main__':
    app.run(debug=True)
