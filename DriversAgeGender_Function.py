# %% [markdown]
# This Jupyter notebook uses plotly.express to build a graph that categorizes the age and gender of drivers involved in incidents for 2023-2024.

# %%
# Import modules
import sqlite3
import pandas as pd
import plotly.express as px

# %% [markdown]
# Define the function to create the bar chart


def create_age_gender_bar_chart(database_path):
    # SQL query to get the data
    query = """
    SELECT
        strftime('%Y', i.CollisionDate) AS Year,
        COALESCE(p.Gender, 'NA') AS Gender,
        CASE
            WHEN p.AgeAtIncident < 20 THEN '<20'
            WHEN p.AgeAtIncident BETWEEN 21 AND 25 THEN '21-25'
            WHEN p.AgeAtIncident BETWEEN 26 AND 30 THEN '26-30'
            WHEN p.AgeAtIncident BETWEEN 31 AND 35 THEN '31-35'
            WHEN p.AgeAtIncident BETWEEN 36 AND 40 THEN '36-40'
            WHEN p.AgeAtIncident BETWEEN 41 AND 45 THEN '41-45'
            WHEN p.AgeAtIncident BETWEEN 46 AND 50 THEN '46-50'
            WHEN p.AgeAtIncident BETWEEN 51 AND 55 THEN '51-55'
            WHEN p.AgeAtIncident BETWEEN 56 AND 60 THEN '56-60'
            WHEN p.AgeAtIncident BETWEEN 61 AND 65 THEN '61-65'
            ELSE '>65'
        END AS AgeRange,
        COUNT(*) AS DriverCount
    FROM
        ksp_person p
    JOIN
        ksp_incidents i ON p.incidentID = i.incidentID
    WHERE
        p.PersonTypeCde = 1
        AND p.AgeAtIncident IS NOT NULL
        AND p.AgeAtIncident <> 0
    GROUP BY
        Year,
        Gender,
        AgeRange
    ORDER BY
        Year,
        Gender,
        CASE
            WHEN AgeRange = '<20' THEN 1
            WHEN AgeRange = '21-25' THEN 2
            WHEN AgeRange = '26-30' THEN 3
            WHEN AgeRange = '31-35' THEN 4
            WHEN AgeRange = '36-40' THEN 5
            WHEN AgeRange = '41-45' THEN 6
            WHEN AgeRange = '46-50' THEN 7
            WHEN AgeRange = '51-55' THEN 8
            WHEN AgeRange = '56-60' THEN 9
            WHEN AgeRange = '61-65' THEN 10
            ELSE 11
        END;
    """

    # Execute the query and load the data into a pandas DataFrame
    with sqlite3.connect(database_path) as conn:
        df = pd.read_sql_query(query, conn)

    # Create the bar chart using plotly.express
    fig = px.bar(
        df,
        x='Year',
        y='DriverCount',
        color='Gender',
        facet_col='AgeRange',
        barmode='group',
        title='Gender and Age Range by Year and Count for Each Group for January 2023-June 2024',
        labels={
            'DriverCount': 'Number of Drivers',
            'AgeRange': 'Age'
        },
        height=600,
        width=1200
    )

    # Update layout for better readability
    fig.update_layout(
        yaxis_title='Number of Drivers',
        legend_title='Gender'
    )

    return fig

# %% [markdown]
# Call the function to create the visualization


# Define the database path
database_path = 'data/crash_data.db'

# Create the bar chart
fig = create_age_gender_bar_chart(database_path)

# Show the bar chart
fig.show()
