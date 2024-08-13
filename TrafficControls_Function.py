# %% [markdown]
# This Jupyter notebook uses plotly express to build a stacked bar chart to display Traffic Control Devices by Route Type and District in Place for Traffic Incidents in Construction Work Zones on State-maintained Routes 2020-2024.

# %%
import os
import sqlite3
import pandas as pd
import plotly.express as px


def connect_to_database(database_path):
    """Connect to SQLite database."""
    return sqlite3.connect(database_path)


def create_traffic_control_chart(database_path):
    """Create a stacked bar chart showing Traffic Control Devices by Route Type and District."""
    # SQL query to get the consolidated dataset
    query = """
    SELECT
        rc.Route_Type,
        c.TrafficControl,
        cd.KYTC_District_Number AS District,
        COUNT(*) AS Count
    FROM
        ksp_controls c
    JOIN
        Roadway_Characteristics_API rc
        ON c.IncidentID = rc.IncidentID
    JOIN
        county_district_lut cd
        ON rc.County_Name = cd.Cnty_Name_PC
    WHERE
        rc.Government_Level = 'State Maintained Roads'
    GROUP BY
        rc.Route_Type,
        c.TrafficControl,
        District
    ORDER BY
        rc.Route_Type,
        c.TrafficControl,
        District;
    """
    with connect_to_database(database_path) as conn:
        df = pd.read_sql_query(query, conn)

    # Specify the order of route types
    category_order = ['I', 'PKWY', 'US', 'KY']

    # Create a bar chart with Plotly
    fig = px.bar(
        df,
        x='Route_Type',
        y='Count',
        color='TrafficControl',
        facet_col='District',
        title='Traffic Control Devices by Route Type and District in Place for Traffic Incidents in Construction Work Zones on State-maintained Routes 2020-2024',
        labels={'Route_Type': 'Route Type', 'Count': 'Device Count',
                'TrafficControl': 'Traffic Control Device', 'District': 'District'},
        category_orders={'Route_Type': category_order},
        height=800
    )

    return fig

# %% [markdown]
# Call the function to generate and display the visualization


# Define the database path
database_path = os.path.abspath('data/crash_data.db')

# Create and display the traffic control chart
fig_traffic_control = create_traffic_control_chart(database_path)
fig_traffic_control.show()
