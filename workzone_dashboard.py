import base64
import folium
from folium import IFrame
import geopandas as gpd
import holoviews as hv
import hvplot.pandas
import json
import numpy as np
import os
import pandas as pd
import panel as pn
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from colorcet import bmy
from PIL import Image

# Enable Panel extensions
pn.extension('plotly', 'tabulator', template='fast')

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

# Set working directory and initialize the map
cwd = os.getcwd()
m = folium.Map(location=[38, -85.5], zoom_start=8)

# Load the GeoJSON data for counties
counties_gdf = gpd.read_file(
    f'{cwd}/data/reference_data/KY_Counties_WGS84.geojson')

# Extract the bounds for each county
county_bounds = {}
for _, row in counties_gdf.iterrows():
    name = row['NAME']
    bounds = row['geometry'].bounds
    county_bounds[name] = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]

# Convert bounds dictionary to JSON format
bounds_json = json.dumps(county_bounds)

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

# Define the path to your north arrow image
north_arrow_image_path = f'{cwd}/data/reference_data/north_arrow.png'

# Encode the image in base64
with open(north_arrow_image_path, 'rb') as f:
    encoded_image = base64.b64encode(f.read()).decode()

# Create HTML content for the DivIcon
html = f'''
    <div style="
        background-image: url('data:image/png;base64,{encoded_image}');
        background-size: contain;
        background-repeat: no-repeat;
        width: 100px;
        height: 100px;
        border: none;
    "></div>
'''

# Add the north arrow to the map
folium.Marker(
    location=[39.5, -82.5],
    icon=folium.DivIcon(html=html),
).add_to(m)

# Add a tile layer from a REST service
folium.TileLayer(
    tiles='https://stamen-tiles-{z}/{x}/{y}.png',
    attr='Map tiles by <a href="https://stamen.com">Stamen Design</a>, under <a href="https://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="https://openstreetmap.org">OpenStreetMap</a>, under <a href="https://www.openstreetmap.org/copyright">ODbL</a>.',
    name='Stamen Toner',
    control=False
).add_to(m)

# Load the GeoJSON data from the data folder
with open(f'{cwd}/data/api_clean_data/Roadway_Characteristics_API.geojson') as f:
    roads_geojson = json.load(f)

# Load the GeoJSON data for counties and districts
with open(f'{cwd}/data/reference_data/KY_County_Polygons.geojson') as f:
    counties_geojson = json.load(f)

with open(f'{cwd}/data/reference_data/KYTC_Districts_Polygons.geojson') as f:
    districts_geojson = json.load(f)

# Define a function to add simple point markers


def add_simple_marker(geojson, map_obj):
    for feature in geojson['features']:
        coords = feature['geometry']['coordinates']
        props = feature['properties']

        popup_content = f"""
        <div style="width: 125px; height: 80px;">
            <p>County: {props.get('County_Name')}</p>
            <p>Route: {props.get('Route')}</p>
        </div>
        """
        iframe = IFrame(html=popup_content, width=125, height=60)
        popup = folium.Popup(iframe, max_width=150)

        folium.CircleMarker(
            location=[coords[1], coords[0]],
            radius=4,
            color='red',
            fill=True,
            fill_color='orange',
            fill_opacity=0.6,
            popup=popup
        ).add_to(map_obj)

# Define a function to add GeoJSON layers


def add_geojson_layer(geojson_data, layer_name, color, fill_color, opacity, fill_opacity, map_obj, show):
    folium.GeoJson(
        geojson_data,
        name=layer_name,
        show=show,
        style_function=lambda feature: {
            'fillColor': fill_color,
            'color': color,
            'weight': 1.2 if layer_name == "Districts" else 2,
            'opacity': opacity,
            'fillOpacity': fill_opacity
        }
    ).add_to(map_obj)


# Add GeoJSON layers
add_geojson_layer(counties_geojson, "Counties",
                  "#E0D2B8", "#F3EDD3", 0.7, 0.3, m, True)
add_geojson_layer(districts_geojson, "Districts",
                  "black", "none", 1, 0, m, True)

# Add a LayerControl to toggle visibility of the county and district boundary layers
folium.LayerControl().add_to(m)

# Add simple point markers to the map
add_simple_marker(roads_geojson, m)

# Save the map to an HTML file
map_html_path = f"web/KY_Incident_Locations.html"

m.save(map_html_path)

# Embed the map HTML in a Panel pane using an iframe
map_pane = pn.pane.HTML(f"""
    <iframe src="{map_html_path}" width="100%" height="500" style="border:none;"></iframe>
""", sizing_mode='stretch_both', height=500)

# Build the Panel layout
df_pane = pn.widgets.Tabulator(
    df, width=600, sizing_mode='stretch_both', height=400)

# Create the final app layout
app = pn.Column(
    pn.layout.Divider(),
    "### Introduction",
    intro,
    pn.layout.Divider(),
    "### Incident Data",
    df_pane,
    # pn.layout.Divider(),
    # "### Location",
    # map_pane,
    sizing_mode='stretch_both'
)

# Serve the app
app.servable()
