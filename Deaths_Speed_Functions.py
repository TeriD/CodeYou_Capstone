# %% [markdown]
# This Jupyter notebook uses plotly to build six graphs that look at the fatalities that occurred for the incidents reported in this project notebook runs a series of visualizations related to fatalities, injuries, and excessive speed.

# %%
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# %%


def connect_to_database(database_path):
    """Connect to SQLite database."""
    return sqlite3.connect(database_path)

# %% [markdown]
# Define functions for each visualization


def create_fatalities_line_bar_charts(database_path):
    """Create line and bar charts showing total fatalities by year and month."""
    query = """
    SELECT strftime('%Y', CollisionDate) AS Year,
           strftime('%m', CollisionDate) AS Month,
           SUM(NumberKilled) AS TotalDeaths
      FROM ksp_incidents
     WHERE NumberKilled > 0
     GROUP BY Year, Month
     ORDER BY Year, Month;
    """
    with connect_to_database(database_path) as conn:
        df = pd.read_sql_query(query, conn)

    df['Date'] = pd.to_datetime(df['Year'] + '-' + df['Month'] + '-01')

    # Create line graph
    fig_line = px.line(df, x='Date', y='TotalDeaths', title='Total Deaths by Year and Month',
                       labels={'TotalDeaths': 'Number of Deaths', 'Date': 'Date'})
    fig_line.update_xaxes(dtick="M3", tickformat="%b %Y",
                          ticklabelmode="period")

    # Create bar chart
    fig_bar = px.bar(df, x='Date', y='TotalDeaths', title='Total Deaths by Year and Month',
                     labels={'TotalDeaths': 'Number of Deaths', 'Date': 'Date'})
    fig_bar.update_xaxes(dtick="M3", tickformat="%b %Y",
                         ticklabelmode="period")

    return fig_line, fig_bar


def create_fatalities_injuries_chart(database_path):
    """Create a bar chart showing fatalities and injuries by year and month."""
    query = """
    SELECT strftime('%Y', CollisionDate) AS Year,
           strftime('%m', CollisionDate) AS Month,
           SUM(NumberKilled) AS TotalDeaths,
           SUM(NumberInjured) AS TotalInjuries
      FROM ksp_incidents
     WHERE NumberKilled > 0 OR NumberInjured > 0
     GROUP BY Year, Month
     ORDER BY Year, Month;
    """
    with connect_to_database(database_path) as conn:
        df = pd.read_sql_query(query, conn)

    df['Date'] = pd.to_datetime(df['Year'] + '-' + df['Month'] + '-01')

    # Melt the dataframe
    df_melted = df.melt(id_vars=['Date'], value_vars=['TotalDeaths', 'TotalInjuries'],
                        var_name='Type', value_name='Count')

    # Create the bar chart
    fig = px.bar(df_melted, x='Date', y='Count', color='Type', barmode='group',
                 title='Total Deaths and Injuries by Year and Month',
                 labels={'Count': 'Number of People', 'Date': 'Date'})
    fig.update_xaxes(dtick="M3", tickformat="%b %Y", ticklabelmode="period")

    return fig


def create_person_type_chart(database_path):
    """Create a bar chart showing fatalities and injuries by year, month, and person type."""
    query = """
    SELECT strftime('%Y', k.CollisionDate) AS Year,
           strftime('%m', k.CollisionDate) AS Month,
           p.personTypecde AS PersonType,
           SUM(k.NumberKilled) AS TotalDeaths,
           SUM(k.NumberInjured) AS TotalInjuries
      FROM ksp_incidents k
      JOIN ksp_person p ON k.IncidentID = p.IncidentID
     WHERE k.NumberKilled > 0 OR k.NumberInjured > 0
     GROUP BY Year, Month, PersonType
     ORDER BY Year, Month, PersonType;
    """
    with connect_to_database(database_path) as conn:
        df = pd.read_sql_query(query, conn)

    df['Date'] = pd.to_datetime(df['Year'] + '-' + df['Month'] + '-01')

    # Melt the dataframe
    df_melted = df.melt(id_vars=['Date', 'PersonType'], value_vars=['TotalDeaths', 'TotalInjuries'],
                        var_name='Type', value_name='Count')

    # Create the bar chart
    fig = px.bar(df_melted, x='Date', y='Count', color='Type', barmode='group',
                 facet_col='PersonType', title='Total Deaths and Injuries by Year, Month, and Person Type',
                 labels={'Count': 'Number of People', 'Date': 'Date', 'PersonType': 'Person Type'})
    fig.update_xaxes(dtick="M3", tickformat="%b %Y", ticklabelmode="period")

    return fig


def create_person_type_pie_chart(database_path):
    """Create a pie chart showing total fatalities by person type."""
    query = """
    SELECT strftime('%Y', k.CollisionDate) AS Year,
           p.personTypecde AS PersonType,
           SUM(k.NumberKilled) AS TotalDeaths
      FROM ksp_incidents k
      JOIN ksp_person p ON k.IncidentID = p.IncidentID
     WHERE k.NumberKilled > 0
     GROUP BY Year, PersonType
     ORDER BY Year, PersonType;
    """
    with connect_to_database(database_path) as conn:
        df = pd.read_sql_query(query, conn)

    # Map person type codes to their labels
    person_type_labels = {
        '1': 'Driver',
        '2': 'Passenger',
        '3': 'Pedestrian',
        '4': 'Animal-Drawn/Ridden',
        '5': 'Bicyclist',
        '6': 'Train Engineer',
        '7': 'Witness',
        '8': 'Owner',
        '9': 'Property Damage Owner'
    }
    df['PersonType'] = df['PersonType'].map(person_type_labels)

    # Create the pie chart
    fig = px.pie(df, values='TotalDeaths', names='PersonType',
                 title='Total Deaths Categorized by Person Type 2020 - 2024',
                 labels={'TotalDeaths': 'Number of Deaths', 'PersonType': 'Person Type'})

    return fig


def create_incidents_by_route_type_chart(database_path):
    """Create a bar chart showing incidents by year and route type involving excessive speed."""
    query = """
    SELECT DISTINCT(i.incidentid), strftime('%Y', i.CollisionDate) AS Year,
           r.Route_Type, r.Speed_Limit_Posted_MPH as Posted_Speed_Limit
      FROM ksp_incidents as i
      JOIN Roadway_Characteristics_API as r
      JOIN ksp_factors as f
        ON i.IncidentID = r.IncidentID
     WHERE f.Factor = 7 AND r.Route_type IN ('I', 'PKWY', 'US', 'KY')
     GROUP BY i.incidentid, Year, r.Route_Type;
    """
    with connect_to_database(database_path) as conn:
        df = pd.read_sql_query(query, conn)

    # Create a count of incidents by year and route type
    df_count = df.groupby(['Year', 'Route_Type']).size(
    ).reset_index(name='IncidentCount')

    # Specify the order of route types
    category_order = ['I', 'PKWY', 'US', 'KY']

    # Create the bar chart
    fig = px.bar(df_count, x='Year', y='IncidentCount', color='Route_Type', barmode='group',
                 title='Incidents by Year and Route Type Involving Excessive Speed as a Factor',
                 labels={'IncidentCount': 'Number of Incidents',
                         'Year': 'Year', 'Route_Type': 'Route Type'},
                 category_orders={'Route_Type': category_order})

    return fig

# %% [markdown]
# Call the functions to generate and display the visualizations


# Define the database path
database_path = os.path.abspath('data/crash_data.db')

# Create and display visualizations
fig_line, fig_bar = create_fatalities_line_bar_charts(database_path)
fig_line.show()
fig_bar.show()

fig_fatalities_injuries = create_fatalities_injuries_chart(database_path)
fig_fatalities_injuries.show()

fig_person_type = create_person_type_chart(database_path)
fig_person_type.show()

fig_person_type_pie = create_person_type_pie_chart(database_path)
fig_person_type_pie.show()

fig_incidents_by_route_type = create_incidents_by_route_type_chart(
    database_path)
fig_incidents_by_route_type.show()
