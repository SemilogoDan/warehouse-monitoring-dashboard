import random
from datetime import datetime, timedelta
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px
import pandas as pd

# Initialize Dash app
app = Dash(__name__)
app.title = "Semilogo Designed Warehouse Monitoring Dashboard"
server = app.server

# --- Data Generation ---
def generate_data(n=1000):
    """
    Generates a Pandas DataFrame with simulated warehouse data.

    Args:
        n (int): The number of data points to generate.  Defaults to 1000.

    Returns:
        pandas.DataFrame: A DataFrame with columns:
            - timestamp (datetime): Timestamps within the last 24 hours.
            - machine_id (str): Machine identifiers (e.g., "M-1", "M-2").
            - task_duration (float): Task durations in minutes.
            - status (str): "success" or "failure".
            - error_code (str): Error codes (e.g., "E-100") or "None".
    """
    now = datetime.now()
    past_limit = now - timedelta(days=1)  # Ensure data is within the last 24 hours
    timestamps = []
    for _ in range(n):
        random_minutes = random.randint(0, 1440)
        timestamps.append(now - timedelta(minutes=random_minutes))

    status = [random.choice(['success'] * 9 + ['failure']) for _ in range(n)]
    error_codes = [random.choice(["E-100", "E-200", "E-300"] if s == "failure" else ["None"]) for s in status]
    return pd.DataFrame({
        "timestamp": timestamps,
        "machine_id": [f"M-{random.randint(1, 5)}" for _ in range(n)],
        "task_duration": [round(random.uniform(5.0, 60.0), 2) for _ in range(n)],
        "status": status,
        "error_code": error_codes
    })

# Generate the initial data
df = generate_data()
df["timestamp"] = pd.to_datetime(df["timestamp"])  # Ensure timestamp is datetime type

# --- Dashboard Layout ---
app.layout = html.Div(
    style={
        "fontFamily": "'Arial', sans-serif",  # Consistent font
        "margin": "20px",
        "backgroundColor": "#f4f4f4",  # Light background
        "color": "#333"  # Darker text for readability
    },
    children=[
        # Header Section
        html.Div(
            style={
                "textAlign": "center",
                "padding": "20px",
                "backgroundColor": "#337ab7",  # Bootstrap primary blue
                "color": "white",
                "marginBottom": "20px",
                "borderRadius": "8px"  # Rounded corners for a softer look
            },
            children=[
                html.H1("🏭 Semilogo Warehouse Operations Dashboard", style={"fontSize": "2.8em"}),  # Larger heading
                html.P("Monitor real-time performance and identify potential issues", style={"fontSize": "1.2em"})  # Subtitle
            ]
        ),

        # Filters Section
        html.Div(
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "20px",  # Space between filter elements
                "marginBottom": "30px",
                "alignItems": "center"  # Vertically center items
            },
            children=[
                html.Div(
                    style={"flex": 1, "minWidth": "200px"},  # Flexible width, minimum width
                    children=[
                        html.Label("📅 Date Range:", style={"fontWeight": "bold", "display": "block", "marginBottom": "5px"}),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=df["timestamp"].min().date(),
                            max_date_allowed=df["timestamp"].max().date(),
                            start_date=df["timestamp"].min().date(),
                            end_date=df["timestamp"].max().date(),
                            style={"width": "100%"}  # Full width within the container
                        )
                    ]
                ),
                html.Div(
                    style={"flex": 1, "minWidth": "200px"},
                    children=[
                        html.Label("⚙️ Machine:", style={"fontWeight": "bold", "display": "block", "marginBottom": "5px"}),
                        dcc.Dropdown(
                            id="machine-dropdown",
                            options=[{"label": m, "value": m} for m in sorted(df["machine_id"].unique())],
                            placeholder="Select a Machine",
                            style={"width": "100%"}
                        )
                    ]
                ),
                html.Div(
                    style={"flex": 1, "minWidth": "200px"},
                    children=[
                        html.Label("🚨 Error Code:", style={"fontWeight": "bold", "display": "block", "marginBottom": "5px"}),
                        dcc.Dropdown(
                            id="error-code-dropdown",
                            options=[{"label": ec, "value": ec} for ec in sorted(df["error_code"].unique()) if ec != "None"],
                            placeholder="Filter by Error Code(s)",
                            multi=True,
                            style={"width": "100%"}
                        )
                    ]
                ),
            ]
        ),

        # KPIs Section
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",  # Responsive grid layout
                "gap": "20px",
                "marginBottom": "30px"
            },
            children=[
                html.Div(
                    style={"backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"},  # Styled container
                    children=[
                        html.H3("Total Tasks", style={"color": "#5cb85c"}),  # Green for success-related
                        html.P(id="total-tasks-kpi", style={"fontSize": "1.8em", "fontWeight": "bold"})  # Large, bold number
                    ]
                ),
                html.Div(
                    style={"backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"},
                    children=[
                        html.H3("Success Rate", style={"color": "#5bc0de"}),  # Cyan for info
                        html.P(id="success-rate-kpi", style={"fontSize": "1.8em", "fontWeight": "bold"})
                    ]
                ),
                html.Div(
                    style={"backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"},
                    children=[
                        html.H3("Avg. Duration (min)", style={"color": "#f0ad4e"}),  # Orange for warning/attention
                        html.P(id="avg-duration-kpi", style={"fontSize": "1.8em", "fontWeight": "bold"})
                    ]
                ),
                html.Div(
                    style={"backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"},
                    children=[
                        html.H3("Failure Rate", style={"color": "#d9534f"}),  # Red for error
                        html.P(id="failure-rate-kpi", style={"fontSize": "1.8em", "fontWeight": "bold"})
                    ]
                ),
            ]
        ),

        # Charts Section
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(500px, 1fr))",  # Responsive columns
                "gap": "20px",  # Space between charts
                "marginBottom": "30px"
            },
            children=[
                dcc.Graph(id="task-status-chart", style={"backgroundColor": "white", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}),  # Styled chart container
                dcc.Graph(id="duration-over-time-chart", style={"backgroundColor": "white", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}),
                dcc.Graph(id="error-distribution-chart", style={"backgroundColor": "white", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}),
                dcc.Graph(id="machine-performance-chart", style={"backgroundColor": "white", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}),
                # New Chart: Status Over Time
                dcc.Graph(id="status-over-time-chart", style={"backgroundColor": "white", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}),
            ]
        ),

        # Data Table Section
        html.Div(
            style={"marginBottom": "20px"},
            children=[
                html.H2("Detailed Task Logs", style={"color": "#337ab7", "marginBottom": "15px"}),  # Styled heading
                dash_table.DataTable(
                    id="task-log-table",
                    columns=[{"name": i, "id": i} for i in df.columns],  # Use DataFrame columns
                    page_size=10,  # Initial page size
                    style_cell={"textAlign": "left", "padding": "8px"},  # Consistent cell styling
                    style_header={"backgroundColor": "#eee", "fontWeight": "bold"},  # Header styling
                    style_data_conditional=[  # Conditional styling for failed tasks
                        {
                            "if": {"filter_query": '{status} = "failure"'},
                            "backgroundColor": "#fdecea",  # Light red
                            "color": "#d9534f",  # Darker red text
                        }
                    ],
                    sort_action="native",  # Enable sorting
                    filter_action="native"  # Enable filtering
                ),
            ]
        ),

        # Footer Section
        html.Footer(
            style={"textAlign": "center", "marginTop": "30px", "padding": "10px", "fontSize": "0.9em", "color": "#777"},  # Centered, smaller text
            children=[
                html.P("© 2025 Semilogo Warehouse Monitoring System")
            ]
        )
    ]
)

# --- Callbacks ---
@app.callback(
    [Output("task-status-chart", "figure"),
     Output("duration-over-time-chart", "figure"),
     Output("error-distribution-chart", "figure"),
     Output("machine-performance-chart", "figure"),
     Output("task-log-table", "data"),
     Output("total-tasks-kpi", "children"),
     Output("success-rate-kpi", "children"),
     Output("avg-duration-kpi", "children"),
     Output("failure-rate-kpi", "children"),
     Output("status-over-time-chart", "figure")],  # Add the new output
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("machine-dropdown", "value"),
     Input("error-code-dropdown", "value")]
)
def update_dashboard(start_date, end_date, machine_id, error_codes):
    """
    Callback function to update the dashboard based on user-selected filters.

    Args:
        start_date (str): Start date from the date range picker.
        end_date (str): End date from the date range picker.
        machine_id (str): Selected machine ID from the dropdown.
        error_codes (list): Selected error codes from the dropdown.

    Returns:
        tuple: A tuple containing updated Plotly figures and KPI values.
    """
    filtered_df = df.copy()  # Create a copy to avoid modifying the original DataFrame

    # --- Filtering ---
    if start_date:
        filtered_df = filtered_df[filtered_df["timestamp"].dt.date >= pd.to_datetime(start_date).date()]
    if end_date:
        filtered_df = filtered_df[filtered_df["timestamp"].dt.date <= pd.to_datetime(end_date).date()]
    if machine_id:
        filtered_df = filtered_df[filtered_df["machine_id"] == machine_id]
    if error_codes:
        filtered_df = filtered_df[filtered_df["error_code"].isin(error_codes)]

    # --- KPI Calculations ---
    total_tasks = len(filtered_df)
    success_count = len(filtered_df[filtered_df["status"] == "success"])
    success_rate = f"{((success_count / total_tasks) * 100):.2f}%" if total_tasks > 0 else "0%"
    avg_duration = f"{filtered_df['task_duration'].mean():.2f}" if not filtered_df.empty else "0.00"
    failure_rate = f"{(((total_tasks - success_count) / total_tasks) * 100):.2f}%" if total_tasks > 0 else "0%"

    # --- Charts ---
    task_status_fig = px.pie(
        filtered_df,
        names="status",
        title="Task Status Distribution",
        color_discrete_sequence=["#5cb85c", "#d9534f"],  # Green and Red
        template="plotly_white"  # Clean white background
    )

    duration_over_time_fig = px.scatter(
        filtered_df,
        x="timestamp",
        y="task_duration",
        color="machine_id",
        title="Task Duration Over Time",
        labels={"timestamp": "Timestamp", "task_duration": "Duration (min)"},  # Clear labels
        template="plotly_white"
    )

    error_distribution_fig = px.bar(
        filtered_df[filtered_df["status"] == "failure"],  # Only show errors
        x="error_code",
        color="error_code",
        title="Error Code Distribution",
        template="plotly_white"
    )

    machine_performance_fig = px.bar(
        filtered_df.groupby("machine_id")["status"].count().reset_index(name="count"),
        x="machine_id",
        y="count",
        color="machine_id",
        title="Tasks per Machine",
        labels={"machine_id": "Machine", "count": "Number of Tasks"},
        template="plotly_white"
    )

    # --- New Chart: Status Over Time ---
    print("First few timestamps in filtered_df:")  # Debugging: Print timestamps
    print(filtered_df['timestamp'].head())
    status_over_time = filtered_df.groupby(pd.Grouper(key='timestamp', freq='M'))['status'].value_counts(normalize=True).mul(100).rename('percentage').reset_index()
    status_over_time_fig = px.line(status_over_time, x='timestamp', y='percentage', color='status',
                                  title='Task Status Over Time',
                                  labels={'timestamp': 'Month', 'percentage': 'Percentage', 'status': 'Status'},
                                  color_discrete_sequence=["#5cb85c", "#d9534f"],
                                  template="plotly_white")

    return (
        task_status_fig,
        duration_over_time_fig,
        error_distribution_fig,
        machine_performance_fig,
        filtered_df.to_dict("records"),
        total_tasks,
        success_rate,
        avg_duration,
        failure_rate,
        status_over_time_fig  # Return the new figure
    )

if __name__ == '__main__':
    app.run_server(debug=True)
