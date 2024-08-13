import base64
import folium
from folium import IFrame
import geopandas as gpd
import json
import os
import pandas as pd
import panel as pn
import plotly.express as px
import plotly.graph_objects as go
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.widgets import DataTable, TableColumn
import sqlite3
import matplotlib.pyplot as plt

# Enable Panel extensions
pn.extension('plotly', 'tabulator', 'bokeh', template='fast')

# Intro
instruction_text = """
<div style='color: black;'>
    <h3 style='font-weight: bold;'>Data Analysis and Visualization of Work Zone Collisions</h3>
    This dashboard visualizes collision locations within construction work zones along
    Kentucky highways and explores some of the statistics by comparing them to each
    other and to roadway characteristics by looking at variables such as age and gender
    of persons involved, number and categories of vehicles, weather, and road conditions.
</div>
"""

instruction = pn.pane.Markdown(instruction_text, width=600)

# Create the workzone_logo with the correct pane method
workzone_logo = pn.pane.Image(
    'Report_Images/KYTCWorkZoneSafety.png', width=200, align='center'
)

# Add custom CSS
pn.config.raw_css = [
    """
    .white-background {
        background-color: white;
    }
    """
]

# Create the row with white background
intro = pn.Row(
    workzone_logo,
    instruction,
    sizing_mode='stretch_width',
    css_classes=['white-background']
)

# Define the path for the SQLite database
database_path = 'data/crash_data.db'

# Check if the database file exists
if not os.path.exists(database_path):
    print(f"Error: The database file '{database_path}' does not exist.")
else:
    try:
        # Connect to the database
        conn = sqlite3.connect(database_path)

        query = """
                SELECT i.IncidentID, i.County, i.CollisionDate,
                    i.MotorVehiclesInvolved as Vehicles_Involved,
                    i.NumberKilled AS Fatalities,
                    i.NumberInjured AS Injuries, i.Weather,
                    i.RdwyConditionCode AS Rdwy_Condition, i.MannerofCollision,
                    i.RdwyCharacter, i.LightCondition,
                    r.Road_Name, r.Milepoint,
                    r.Speed_Limit_Posted_MPH AS Speed_Limit
                FROM ksp_incidents AS i
                JOIN Roadway_Characteristics_API AS r
                    ON i.IncidentID = r.IncidentID
                WHERE r.Route_Type IN ('I', 'PKWY', 'US', 'KY')
                """

        # Execute the query and fetch the results into a DataFrame
        df = pd.read_sql_query(query, conn)

    except sqlite3.OperationalError as e:
        print(f"OperationalError: {e}")
    finally:
        if conn:
            conn.close()

# Placeholder functions for other visualizations


def humanFactors():
    conn = sqlite3.connect(f'{os.getcwd()}/data/crash_data.db')
    query = """
    SELECT t1.Factor, t2.Description
    FROM ksp_factors t1
    JOIN unit_factor_code_lut t2
        ON t1.Factor = t2.Factor_Code
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    factor_counts = df['Description'].value_counts()
    top_10_factors = factor_counts.head(10)
    top_10_factors_df = pd.DataFrame({
        'Factor': top_10_factors.index,
        'Count': top_10_factors.values,
    })

    plt.figure(figsize=(9, 6))
    plt.bar(top_10_factors_df['Factor'],
            top_10_factors_df['Count'], color='skyblue')
    plt.xlabel('Human Factors')
    plt.ylabel('Count')
    plt.title('Top Human Factors')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return pn.pane.Markdown(f"![bar_chart](data:image/png;base64,{image_base64})")


def deaths_speed():
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

    return pn.pane.Markdown(fig)


def driversAgeGender():
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
    return pn.pane.Markdown(fig)


def incidentsbyDistrictYear():
    # Initialize the Dash app
    app = dash.Dash(__name__)

    # Define the layout of the app
    app.layout = html.Div([
        html.H1("Collision Incidents by KYTC District and Year"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': str(year)} for year in range(
                2020, 2025)],  # Example range of years
            value='2020',  # Default value
            clearable=False
        ),
        dcc.Graph(id='incident-bar-chart')
    ])

    # Define a function to fetch data and create the Plotly figure
    def get_figure(selected_year):
        # Connect to the SQLite database
        conn = sqlite3.connect(os.path.join(os.getcwd(), 'data/crash_data.db'))

        # Define the query
        query = f'''
        SELECT t1.IncidentID, t2.KYTC_District_Number AS District, t2.D_District,
            t2.Cnty_Name_PC, strftime("%Y", t1.CollisionDate) AS CollisionYear,
            COUNT(*) AS IncidentCount
        FROM ksp_incidents t1
        JOIN county_district_lut t2
            ON t1.County = t2.Cnty_Name_UC
        WHERE strftime("%Y", t1.CollisionDate) = '{selected_year}'
        GROUP BY
            District
        ORDER BY
            District;
        '''

        # Execute the query and fetch the results into a DataFrame
        df = pd.read_sql_query(query, conn)
        print(df)

        # Close the database connection
        conn.close()

        # Define the color sequence you want to use
        color_sequence = px.colors.qualitative.Vivid_r

        # Create the bar chart using Plotly Express
        fig = px.bar(df, x='District', y='IncidentCount', color='District',
                     color_discrete_sequence=color_sequence,
                     labels={'IncidentCount': 'Number of Incidents'},
                     title=f'Number of Incidents by District for {selected_year}')

        return fig

        # Define the callback to update the graph
        @app.callback(
            Output('incident-bar-chart', 'figure'),
            [Input('year-dropdown', 'value')]
        )
        def update_graph(selected_year):
            return get_figure(selected_year)

        return app

    return pn.pane.Markdown(app)


def VehicleType_Bokeh():
    # Connect to SQLite database
    cwd = os.getcwd()
    conn = sqlite3.connect(cwd + '/data/crash_data.db')

    # Execute SQL query and load results into a DataFrame
    query = """
    SELECT DISTINCT(UnitType), COUNT(*) as count
    FROM ksp_vehicles
    GROUP BY UnitType
    HAVING COUNT(*) > 1
    """
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Prepare data for the pie chart
    df['angle'] = df['count']/df['count'].sum() * 2*pi
    df['color'] = Category20c[len(df)]

    # Create a Bokeh pie chart
    p = figure(height=550, width=800, title="Vehicle Types Involved in Work Zone Collisions (2020-2024)", toolbar_location=None,
               tools="hover", tooltips="@UnitType: @count", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='UnitType', source=ColumnDataSource(df))

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    # Adjust legend properties
    p.legend.title = 'Vehicle Types'
    p.legend.location = 'top_right'
    p.legend.orientation = 'vertical'
    p.legend.label_text_font_size = '8pt'

    output_file("web/vehicle_types.html")
    return pn.pane.Bokeh(p)


# Create the final app layout
app = pn.Column(
    pn.layout.Divider(),
    "### Introduction",
    intro,
    pn.layout.Divider(),
    "### Incident Data",
    pn.widgets.Tabulator(df, width=800, height=250),
    # pn.layout.Divider(),
    # "### Location",
    # create_folium_map(),
    pn.layout.Divider(),
    "### Human Factors",
    humanFactors(),
    pn.layout.Divider(),
    "### Deaths vs Speed",
    deaths_speed(),
    pn.layout.Divider(),
    "### Drivers Age and Gender",
    driversAgeGender(),
    pn.layout.Divider(),
    "### Incidents by District and Year",
    incidentsbyDistrictYear(),
    pn.layout.Divider(),
    "### Vehicle Type",
    VehicleType_Bokeh(),
    sizing_mode='stretch_width'
)

# Serve the app
app.servable()
app.show()
