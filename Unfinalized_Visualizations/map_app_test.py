import folium
import json
import panel as pn
from shapely.geometry import shape, MultiPoint

# Load the Panel extension
pn.extension()

# Set working directory and initialize the map
cwd = '/Users/terid/Git/CodeYou_Capstone'  # Update this to your actual directory
m = folium.Map(location=[37.8, -85.5], zoom_start=7)

# Load GeoJSON data
with open(f'{cwd}/data/reference_data/KY_Counties.geojson') as f:
    counties_geojson = json.load(f)

with open(f'{cwd}/data/api_clean_data/Roadway_Characteristics_API.geojson') as f:
    roads_geojson = json.load(f)

# Add custom panes and GeoJSON layers
folium.map.CustomPane('county_pane').add_to(m)
folium.map.CustomPane('road_pane').add_to(m)
county_layer = folium.GeoJson(counties_geojson, name='Counties', pane='county_pane').add_to(m)
roads_layer = folium.GeoJson(roads_geojson, name='Roads', pane='road_pane').add_to(m)

# Create dropdown for selecting counties
counties = {feature['properties']['NAME']: feature for feature in counties_geojson['features']}
county_names = list(counties.keys())

def zoom_to_county(event):
    county_name = event.new
    feature = counties[county_name]
    geom = shape(feature['geometry'])
    bounds = geom.bounds
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
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
