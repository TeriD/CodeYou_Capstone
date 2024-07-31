import folium
import json
import os
import panel as pn
from folium import IFrame
from PIL import Image
import base64
import webbrowser

# Load the Panel extension
pn.extension()

# Set working directory and initialize the map
cwd = os.getcwd()
m = folium.Map(location=[38.0, -85.5], zoom_start=8)

# Add custom JavaScript to display cursor location
javascript_code = """
    <script>
    function updateLocation(e) {
        var latlng = e.latlng;
        var lat = latlng.lat.toFixed(6);
        var lng = latlng.lng.toFixed(6);
        document.getElementById('location-info').innerHTML = 'Lat: ' + lat + ' | Lng: ' + lng;
    }

    var map = L.map('map', {
        center: [38.0, -85.5],
        zoom: 8
    });

    map.on('mousemove', updateLocation);

    var infoControl = L.control({position: 'bottomleft'});
    infoControl.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info');
        this._div.id = 'location-info';
        this._div.innerHTML = 'Lat: -- | Lng: --';
        return this._div;
    };
    infoControl.addTo(map);
    </script>
"""

# Add the JavaScript to the map
m.get_root().html.add_child(folium.Element(javascript_code))

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
        width: 100px;  /* Adjust size as needed */
        height: 100px; /* Adjust size as needed */
        border: none;
    "></div>
'''

# Add the north arrow to the map
folium.Marker(
    # Adjust the location to where you want the north arrow
    location=[39.5, -82.5],
    icon=folium.DivIcon(html=html),
).add_to(m)

# Add a tile layer from a REST service
folium.TileLayer(
    tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
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
        # Extract coordinates and properties
        coords = feature['geometry']['coordinates']
        props = feature['properties']

        # Create an HTML string for the popup
        popup_content = f"""
        <div style="width: 125px; height: 80px;">
            <p>County: {props.get('County_Name')}</p>
            <p>Route: {props.get('Route')}</p>
        </div>
        """
        iframe = IFrame(html=popup_content, width=125, height=60)
        popup = folium.Popup(iframe, max_width=150)

        # Create a simple circular marker
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

# Create a county selector and add JavaScript for zoom functionality
county_selector_js = """
    <script>
    function zoomToCounty(countyName) {
        var counties = {{ counties }};
        var selectedCounty = counties.find(function(county) {
            return county.properties.COUNTY_NAM === countyName;
        });
        if (selectedCounty) {
            var bounds = L.geoJSON(selectedCounty).getBounds();
            map.fitBounds(bounds);
        }
    }

    var countyNames = {{ county_names }};
    var select = L.DomUtil.create('select', 'county-selector');
    select.onchange = function() {
        var countyName = select.value;
        zoomToCounty(countyName);
    };

    countyNames.forEach(function(countyName) {
        var option = L.DomUtil.create('option', '', select);
        option.value = countyName;
        option.innerHTML = countyName;
    });

    var selectorControl = L.control({ position: 'topright' });
    selectorControl.onAdd = function(map) {
        return select;
    };
    selectorControl.addTo(map);
    </script>
"""

# Prepare the county data and names for JavaScript injection
counties_data = json.dumps(counties_geojson['features'])
county_names = [feature['properties']['NAME']
                for feature in counties_geojson['features']]
county_names = json.dumps(county_names)

# Add the county selector JavaScript to the map
county_selector_js = county_selector_js.replace(
    '{{ counties }}', counties_data)
county_selector_js = county_selector_js.replace(
    '{{ county_names }}', county_names)
m.get_root().html.add_child(folium.Element(county_selector_js))

# Save the map to an HTML file
m.save(f"{cwd}/web/KY_Incident_Locations.html")

# HTML content for the title block
title_html = '''
<!DOCTYPE html>
<html>
<head>
    <style>
        .title-block {
            position: absolute;
            top: 10px;
            left: 30%;
            transform: translateX(-50%);
            background-color: white;
            padding: 10px;
            border: 2px solid black;
            z-index: 1000;
        }
    </style>
</head>
<body>
    <div class="title-block">
        <h1>Collision Incidents within Construction Work Zones in Kentucky 2020-2024</h1>
        <p>** Data from Kentucky State Police Public Collision Data **</p>
    </div>
</body>
</body>
</html>
'''

# Read the existing HTML file
file_path = f'{cwd}/web/KY_Incident_Locations.html'
with open(file_path, 'r') as file:
    map_html = file.read()

# Insert the title block HTML into the map HTML
head_pos = map_html.find('<body>') + len('<body>')
map_html = map_html[:head_pos] + title_html + map_html[head_pos:]

# Write the modified HTML back to the file
with open(file_path, 'w') as file:
    file.write(map_html)

# Open the HTML file in the default web browser
webbrowser.open(f'file://{file_path}')
