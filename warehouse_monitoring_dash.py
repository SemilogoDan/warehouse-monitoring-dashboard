import random
from datetime import datetime, timedelta
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Initialize Dash app
app = Dash(__name__)
app.title = "Warehouse Monitoring Dashboard"
server = app.server

# Generate initial data
def generate_data(n=1000):
    now = datetime.now()
    status = [random.choice(['success'] * 9 + ['failure']) for _ in range(n)]
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

df = generate_data()
df["timestamp"] = pd.to_datetime(df["timestamp"])

# App layout
app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "margin": "0 auto",
        "maxWidth": "1200px",
        "padding": "20px"
    },
    children=[
        html.H1("📊 Warehouse Monitoring Dashboard", style={"textAlign": "center", "marginBottom": "40px"}),

        html.Div(
            style={"display": "flex", "justifyContent": "space-between", "flexWrap": "wrap", "marginBottom": "30px"},
            children=[
                html.Div([
                    html.Label("📅 Select Date Range"),
                    dcc.DatePickerRange(
                        id="date-range",
                        min_date_allowed=df["timestamp"].min(),
                        max_date_allowed=df["timestamp"].max(),
                        start_date=df["timestamp"].min(),
                        end_date=df["timestamp"].max()
                    )
                ], style={"marginBottom": "20px"}),

                html.Div([
                    html.Label("⚙️ Select Machine"),
                    dcc.Dropdown(
                        id="machine-dropdown",
                        options=[{"label": m, "value": m} for m in df["machine_id"].unique()],
                        placeholder="Select Machine",
                        style={"width": "200px"}
                    )
                ])
            ]
        ),

        html.Div([
            dcc.Graph(id="incident-graph"),
            dcc.Graph(id="duration-graph"),
        ], style={"marginBottom": "30px"}),

        html.H3("📋 Task Logs"),
        dash_table.DataTable(
            id="log-table",
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "5px"},
            style_header={"backgroundColor": "#f4f4f4", "fontWeight": "bold"},
            style_data_conditional=[
                {
                    "if": {"filter_query": '{status} = "failure"'},
                    "backgroundColor": "#ffe6e6"
                }
            ]
        )
    ]
)

# Callback to update dashboard
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
        title="Error Code Distribution",
        color_discrete_sequence=["indianred"]
    )

    fig2 = px.scatter(
        filtered_df,
        x="timestamp",
        y="task_duration",
        color="machine_id",
        title="Task Duration Over Time",
        template="plotly_white"
    )

    return fig1, fig2, filtered_df.to_dict("records")

if __name__ == '__main__':
    app.run(debug=True)
