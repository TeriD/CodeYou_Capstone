import folium
import json
import os
import panel as pn
from shapely.geometry import shape, MultiPoint

# Load the Panel extension
pn.extension()

# Set working directory and initialize the map
# Update this to your actual directory
cwd = os.getcwd()
m = folium.Map(location=[37.8, -85.5], zoom_start=7)

# Load GeoJSON data
with open(f'{cwd}/data/api_clean_data/Roadway_Characteristics_API.geojson') as f:
    roads_geojson = json.load(f)

# Extract county names from the roads GeoJSON
counties = {}
for feature in roads_geojson['features']:
    county_name = feature['properties'].get(
        'County_Name', 'Unknown')  # Adjust key as needed
    if county_name not in counties:
        counties[county_name] = []
    counties[county_name].append(feature)

# Add GeoJSON data to the map
roads_layer = folium.GeoJson(roads_geojson, name='Roads').add_to(m)

# Create dropdown for selecting counties
county_names = list(counties.keys())


def zoom_to_county(event):
    county_name = event.new
    features = counties.get(county_name, [])
    if not features:
        return
    # Create a MultiPoint geometry for the selected county
    points = [shape(feature['geometry']) for feature in features]
    multi_point = MultiPoint(points)
    bounds = multi_point.bounds
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    # Optional: Highlight points
    folium.GeoJson({
        'type': 'FeatureCollection',
        'features': features
    }, style_function=lambda x: {'color': 'red'}).add_to(m)
    map_html = m.get_root().render()
    map_pane.object = map_html


dropdown = pn.widgets.Select(name='Select County', options=county_names)
dropdown.param.watch(zoom_to_county, 'value')

# Embed the map and dropdown in a Panel layout
map_html = m.get_root().render()
map_pane = pn.pane.HTML(map_html, sizing_mode='stretch_both')

app = pn.Column(dropdown, map_pane)

# Serve the app
app.show(port=5006)
