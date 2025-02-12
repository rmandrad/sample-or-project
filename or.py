import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Load sample data from CSV file
def load_data():
    file_path = "sample_risk_scoring_banking_solution_data.csv"  # Path to the updated banking solutions dataset
    df = pd.read_csv(file_path)
    return df

# Initialize Dash app
app = dash.Dash(__name__)
df = load_data()

app.layout = html.Div([
    html.H1("Operational Resilience Risk Analysis - Banking Solutions"),
    
    # Dropdown to filter by Banking Solution
    html.Label("Select Banking Solution:"),
    dcc.Dropdown(
        id="solution-dropdown",
        options=[
            {"label": solution, "value": solution} for solution in df["Banking Solution"].unique()
        ],
        value=df["Banking Solution"].unique()[0],
        clearable=False
    ),
    
    # Solution Risk Score Display
    html.H2("Solution Risk Score"),
    html.Div(id="solution-risk-score"),
    
    # Risk Score Distribution
    html.H2("Risk Score Distribution"),
    dcc.Graph(id="risk-score-dist"),
    
    # Scatter Plot - MTTR vs. Risk Score
    html.H2("MTTR vs Risk Score"),
    dcc.Graph(id="mttr-risk-scatter"),
    
    # Bar Chart - Risk Score by Application
    html.H2("Risk Score by Application"),
    dcc.Graph(id="risk-score-bar"),
])

@app.callback(
    [
        Output("solution-risk-score", "children"),
        Output("risk-score-dist", "figure"),
        Output("mttr-risk-scatter", "figure"),
        Output("risk-score-bar", "figure")
    ],
    [Input("solution-dropdown", "value")]
)
def update_graphs(selected_solution):
    filtered_df = df[df["Banking Solution"] == selected_solution]
    solution_risk_score = filtered_df["Solution Risk Score"].iloc[0]
    
    # Solution Risk Score Display
    risk_score_text = f"Overall Risk Score for {selected_solution}: {solution_risk_score:.2f}"
    
    # Risk Score Distribution
    dist_fig = {
        "data": [{
            "x": filtered_df["Risk Score"],
            "type": "histogram",
            "opacity": 0.7,
        }],
        "layout": {
            "xaxis": {"title": "Risk Score"},
            "yaxis": {"title": "Frequency"},
        },
    }
    
    # Scatter Plot - MTTR vs. Risk Score
    scatter_fig = {
        "data": [{
            "x": filtered_df["MTTR (hrs)"],
            "y": filtered_df["Risk Score"],
            "mode": "markers",
            "marker": {"size": 10},
        }],
        "layout": {
            "xaxis": {"title": "MTTR (hrs)"},
            "yaxis": {"title": "Risk Score"},
        },
    }
    
    # Bar Chart - Risk Score by Application
    bar_fig = {
        "data": [{
            "x": filtered_df["Application_ID"],
            "y": filtered_df["Risk Score"],
            "type": "bar",
        }],
        "layout": {
            "xaxis": {"title": "Application ID", "tickangle": -45},
            "yaxis": {"title": "Risk Score"},
        },
    }
    
    return risk_score_text, dist_fig, scatter_fig, bar_fig

if __name__ == "__main__":
    app.run_server(debug=False)

