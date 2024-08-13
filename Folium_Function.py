# %% [markdown]
# This Jupyter Notebook creates a Folium map from the imported geojson file created earlier in the processing of the API dataset.

# %%
import folium
import geopandas as gpd
import json
import os
import panel as pn
from folium import IFrame
from PIL import Image
import base64
import webbrowser


def initialize_map(center_lat=38, center_lon=-85.5, zoom_start=8):
    """Initialize the Folium map."""
    return folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start)


def load_county_bounds(geojson_path):
    """Load county boundary GeoJSON file and extract bounding boxes."""
    counties_gdf = gpd.read_file(geojson_path)
    county_bounds = {}
    for _, row in counties_gdf.iterrows():
        name = row['NAME']  # Replace 'NAME' with the correct column name
        bounds = row['geometry'].bounds
        county_bounds[name] = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
    return county_bounds


def add_custom_javascript(map_obj, bounds_json):
    """Add custom JavaScript to the Folium map for interactive features."""
    javascript_code = f"""
    <script>
    function updateLocation(e) {{
        var latlng = e.latlng;
        var lat = latlng.lat.toFixed(6);
        var lng = latlng.lng.toFixed(6);
        document.getElementById('location-info').innerHTML = 'Lat: ' + lat + ' | Lng: ' + lng;
    }}

    function zoomToCounty() {{
        var selectedCounty = document.getElementById('county-select').value;
        var bounds = boundsDict[selectedCounty];
        if (bounds) {{
            var latlngs = [
                [bounds[0][0], bounds[0][1]],
                [bounds[1][0], bounds[1][1]]
            ];
            var bounds = L.latLngBounds(latlngs);
            map.fitBounds(bounds);
        }}
    }}

    var map = L.map('map', {{
        center: [38.0, -85.5],
        zoom: 8
    }});

    map.on('mousemove', updateLocation);

    var infoControl = L.control({{position: 'bottomleft'}});
    infoControl.onAdd = function (map) {{
        this._div = L.DomUtil.create('div', 'info');
        this._div.id = 'location-info';
        this._div.innerHTML = 'Lat: -- | Lng: --';
        return this._div;
    }};
    infoControl.addTo(map);

    var selectorControl = L.control({{position: 'bottomright'}});
    selectorControl.onAdd = function (map) {{
        this._div = L.DomUtil.create('div', 'selector');
        this._div.innerHTML = `
            <label for="county-select">Select a county:</label>
            <select id="county-select" onchange="zoomToCounty()">
                <option value="">Select...</option>
                {''.join([f'<option value="{name}">{
                         name}</option>' for name in bounds_json.keys()])}
            </select>
        `;
        return this._div;
    }};
    selectorControl.addTo(map);

    var boundsDict = {bounds_json};
    </script>
    """
    map_obj.get_root().html.add_child(folium.Element(javascript_code))


def add_geojson_layer(map_obj, geojson_data, layer_name, color, fill_color, opacity, fill_opacity, show=True):
    """Add GeoJSON layers to the Folium map."""
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


def add_simple_marker(map_obj, geojson_data):
    """Add simple point markers to the Folium map."""
    for feature in geojson_data['features']:
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


def add_north_arrow(map_obj, image_path, location=[39.5, -82.5]):
    """Add a north arrow image to the Folium map."""
    with open(image_path, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode()

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

    folium.Marker(
        location=location,
        icon=folium.DivIcon(html=html),
    ).add_to(map_obj)


def add_custom_css(map_obj):
    """Add custom CSS to the Folium map."""
    custom_css = """
    <style>
        .leaflet-control-layers {
            font-size: 12px;
        }
        .leaflet-control-layers-toggle {
            width: 150px;
            height: 150px;
        }
        .leaflet-control-layers-list {
            max-height: 250px;
            overflow-y: auto;
        }
    </style>
    """
    map_obj.get_root().html.add_child(folium.Element(custom_css))


def save_and_open_map(map_obj, file_path):
    """Save the Folium map to an HTML file and open it in a web browser."""
    map_obj.save(file_path)
    webbrowser.open(f'file://{file_path}')


def create_folium_map():
    """Create and configure the Folium map with all components."""
    cwd = os.getcwd()

    # Initialize the map
    m = initialize_map()

    # Load county bounds
    county_bounds = load_county_bounds(
        f'{cwd}/data/reference_data/KY_Counties_WGS84.geojson')
    bounds_json = json.dumps(county_bounds)

    # Add custom JavaScript
    add_custom_javascript(m, bounds_json)

    # Load GeoJSON data
    with open(f'{cwd}/data/api_clean_data/Roadway_Characteristics_API.geojson') as f:
        roads_geojson = json.load(f)
    with open(f'{cwd}/data/reference_data/KY_County_Polygons.geojson') as f:
        counties_geojson = json.load(f)
    with open(f'{cwd}/data/reference_data/KYTC_Districts_Polygons.geojson') as f:
        districts_geojson = json.load(f)

    # Add GeoJSON layers
    add_geojson_layer(m, counties_geojson, "Counties",
                      "#E0D2B8", "#F3EDD3", 0.7, 0.3)
    add_geojson_layer(m, districts_geojson, "Districts", "black", "none", 1, 0)

    # Add markers
    add_simple_marker(m, roads_geojson)

    # Add north arrow
    add_north_arrow(m, f'{cwd}/data/reference_data/north_arrow.png')

    # Add custom CSS
    add_custom_css(m)

    # Add LayerControl
    folium.LayerControl().add_to(m)

    # Save and open the map
    file_path = f"{cwd}/web/KY_Incident_Locations.html"
    save_and_open_map(m, file_path)


# %% [markdown]
# Call the function to create and display the Folium map
create_folium_map()
