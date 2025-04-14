# 🏭 Semilogo Warehouse Monitoring Dashboard

<!--- [![Dashboard Preview](https://via.placeholder.com/800x400?text=Semilogo+Dashboard+Preview)](https://warehouse-monitoring-dashboard.onrender.com/) -->

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-00CA7D?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/dash/)
[![Plotly](https://img.shields.io/badge/Plotly-232F67?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

A comprehensive, real-time monitoring solution for warehouse operations with advanced analytics and interactive visualizations.

**[Live Demo](https://warehouse-monitoring-dashboard.onrender.com/)**
---

### Enhanced Features

#### Advanced Analytics Dashboard
- **Multi-dimensional filtering** by date range, machine ID, and error codes.
- **Real-time KPI tracking** with 4 key metrics.
- **Interactive visualizations** with hover tooltips and zoom capabilities.

#### Visualization Suite
| Chart              | Purpose                           | Insights                        |
|--------------------|-----------------------------------|---------------------------------|
| Task Status Pie    | Overall success/failure ratio     | Operational health              |
| Duration Scatter   | Task duration trends over time    | Performance patterns            |
| Error Distribution | Frequency of error codes          | Identification of problem areas |
| Machine Performance| Workload distribution across machines | Capacity planning               |

#### User Experience
- Modern, responsive UI with professional styling.
- Intuitive filter controls with clear labeling.
- Color-coded status indicators (**red** for failures).
- Mobile-friendly layout (tested down to tablet size).

---

### 🛠️ Technical Implementation

#### Component Architecture
The dashboard is built using the following components and their interactions:

1. **Data Generation**:
   - Simulates or retrieves warehouse logs (e.g., task durations, machine statuses, error codes).

2. **Filter Controls**:
   - Allows users to filter data by date range, machine ID, and error codes.

3. **KPI Cards**:
   - Displays key performance indicators such as total tasks, success rate, and average task duration.

4. **Visualizations**:
   - Includes interactive charts like pie charts, scatter plots, bar charts, and histograms.

5. **Data Table**:
   - Provides a detailed log of all tasks, including timestamps, machine IDs, durations, statuses, and error codes.

6. **User Interface**:
   - Combines all components into a unified dashboard for seamless interaction.

#### Core Technologies
- **Framework**: Dash (Python)
- **Visualization**: Plotly Express
- **Data Processing**: Pandas
- **UI Components**: Dash HTML Components
- **Styling**: CSS-in-Python

---

### Project Structure
warehouse_monitoring_dashboard/
├── warehouse_dashboard.py # Contains the main Dash application logic and layout
├── requirements.txt # Lists the Python dependencies required to run the app
└── README.md # Project documentation (this file)


---

### Deployment Guide

#### Local Development
1. **Clone the repository**:
   ```bash
   git clone https://github.com/SemilogoDan/warehouse-monitoring-dashboard.git
   cd warehouse-monitoring-dashboard

###  Set up the environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt


###  Run the application :
python warehouse_dashboard.py


##  Online Deployment
The dashboard is also deployed and accessible online via Live Demo .

###  Contributing
We welcome contributions to improve the dashboard! Here’s how you can contribute:

###  Fork the Repository :
Create a fork of the project on GitHub.
Make Changes :
Implement your improvements or fixes.
Submit a Pull Request :
Describe your changes and submit a pull request for review.

Please ensure your contributions align with the project's coding standards and goals.
License
This project is licensed under the MIT License . Feel free to use, modify, and distribute it as needed. See the LICENSE file for more details.
