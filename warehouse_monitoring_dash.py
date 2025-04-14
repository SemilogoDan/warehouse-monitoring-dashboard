import random
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px

# ---------------------- Step 1: Simulate warehouse logs ----------------------
def simulate_logs(n=500):
    data = []
    now = datetime.now()
    for _ in range(n):
        timestamp = now - timedelta(minutes=random.randint(0, 1440))
        machine_id = f"M-{random.randint(1, 5)}"
        task_duration = round(random.uniform(5.0, 60.0), 2)
        status = random.choice(["success"] * 9 + ["failure"])
        error_code = random.choice(["E-100", "E-200", "E-300"] if status == "failure" else ["None"])
        data.append((timestamp.strftime("%Y-%m-%d %H:%M:%S"), machine_id, task_duration, status, error_code))
    return data

# ---------------------- Step 2: Save to SQLite database ----------------------
def setup_database():
    conn = sqlite3.connect("warehouse.db")
    c = conn.cursor()
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            machine_id TEXT,
            task_duration REAL,
            status TEXT,
            error_code TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_logs(data):
    conn = sqlite3.connect("warehouse.db")
    c = conn.cursor()
    c.executemany('''INSERT INTO logs (timestamp, machine_id, task_duration, status, error_code)
                     VALUES (?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()

# ---------------------- Step 3: Load data from DB ----------------------
def load_data():
    conn = sqlite3.connect("warehouse.db")
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    conn.close()
    return df

# ---------------------- Step 4: Dash dashboard ----------------------
# Initialize Dash app
app = Dash(__name__)
app.title = "Warehouse Monitoring Dashboard"
# Expose the server for Gunicorn to use
server = app.server  # This is the WSGI app that Gunicorn needs

# Setup DB and insert simulated logs only if empty
setup_database()
df_temp = load_data()
if df_temp.empty:
    insert_logs(simulate_logs())
df = load_data()
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Layout
app.layout = html.Div([ 
    html.H1("Warehouse Monitoring Dashboard", style={"textAlign": "center"}), 

    dcc.DatePickerRange( 
        id="date-range", 
        min_date_allowed=df["timestamp"].min().date(), 
        max_date_allowed=df["timestamp"].max().date(), 
        start_date=df["timestamp"].min().date(), 
        end_date=df["timestamp"].max().date(), 
    ), 

    dcc.Dropdown( 
        id="machine-dropdown", 
        options=[{"label": m, "value": m} for m in df["machine_id"].unique()], 
        value=None, 
        placeholder="Select Machine (Optional)", 
        multi=False, 
        style={"marginTop": "10px"} 
    ), 

    dcc.Graph(id="incident-graph"), 
    dcc.Graph(id="duration-graph"), 
    html.H3("Log Records"), 
    dash_table.DataTable( 
        id="log-table", 
        columns=[{"name": i, "id": i} for i in df.columns], 
        style_table={"overflowX": "auto"}, 
        page_size=10 
    ) 
])

@app.callback( 
    [Output("incident-graph", "figure"), 
     Output("duration-graph", "figure"), 
     Output("log-table", "data")], 
    [Input("date-range", "start_date"), 
     Input("date-range", "end_date"), 
     Input("machine-dropdown", "value")] 
) 
def update_dashboard(start_date, end_date, machine_id): 
    filtered_df = df[(df["timestamp"] >= pd.to_datetime(start_date)) & (df["timestamp"] <= pd.to_datetime(end_date))] 
    if machine_id: 
        filtered_df = filtered_df[filtered_df["machine_id"] == machine_id] 

    err_df = filtered_df[filtered_df["status"] == "failure"] 
    fig1 = px.histogram(err_df, x="error_code", title="Incident Frequency by Error Code")

    fig2 = px.scatter(filtered_df, x="timestamp", y="task_duration", color="machine_id", 
                      title="Task Duration Over Time")

    return fig1, fig2, filtered_df.to_dict("records")

# ---------------------- Run app ----------------------
if __name__ == '__main__': 
    app.run(debug=True)
