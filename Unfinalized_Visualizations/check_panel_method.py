import folium
import json
import panel as pn

# Initialize Panel extension
pn.extension()

# Create the Folium map
m = folium.Map(location=[37.8, -85.5], zoom_start=7)

# Load and add GeoJSON data to the map
cwd = '/Users/terid/Git/CodeYou_Capstone'
with open(f'{cwd}/data/reference_data/KY_Counties.geojson') as f:
    counties_geojson = json.load(f)
folium.GeoJson(counties_geojson).add_to(m)

# Render the map to HTML
map_html = m._repr_html_()

# Create a Panel with the map HTML
map_pane = pn.pane.HTML(map_html, sizing_mode='stretch_both')

# Display the Panel
app = pn.Column(map_pane)
app.show(port=5006)
