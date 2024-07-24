
# Import required modules
import os
import sqlite3
import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.geometry import Point
import json
import requests
from furl import furl
from time import perf_counter
import numpy as np

# ---------------------------------------------------------------------------------------------
# Set Pandas Options
# ---------------------------------------------------------------------------------------------

# set to show the max width of the dataframe when printing
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)


# -------------------------------------------------------------------------------------------
# Variables
# -------------------------------------------------------------------------------------------

# Define the path for the SQLite database
cwd = os.getcwd()
database_path = os.path.join(cwd, 'data', 'crash_data.db')

# Connect to the SQLite database
conn = sqlite3.connect(database_path)

# Build the request url with parameters
url_base = r"https://kytc-api-v100-lts-qrntk7e3ra-uc.a.run.app/api/"

return_keys = r"Cardinality, "\
              r" County_Name, Direction, Government_Level, "\
              r" Grade_Class, Grade_Direction, Grade_Percent, "\
              r" Horizontal_Curve_Degree, Horizontal_Curve_Direction, "\
              r" Lane_Width_Feet, Lanes_Total_Number_Driving, Median_Type, "\
              r" Median_Type_of_Roadway, Median_Width_Feet, Road_Name, "\
              r" Route, Route_Type, Route_Unique_Identifier, "\
              r" Milepoint, Shoulder_Width_Cardinal_Left_Feet, "\
              r" Shoulder_Width_Cardinal_Right_Feet, "\
              r" Shoulder_Width_NonCardinal_Left_Feet, "\
              r" Shoulder_Width_NonCardinal_Right_Feet, "\
              r" Snow_Ice_Priority_Route_Type, Speed_Limit_Official_Order, "\
              r" Speed_Limit_Posted_MPH, Surface_Type, "\
              r" Traffic_Last_Count, Truck_Weight_Limit_Class, "\
              r" Type_Operation, Geometry"

# create a list to store the results in
results = list()
record_count = 0  # Initialize the counter

# ---------------------------------------------------------------------------------------------
# Function to call API for roadway characteristics from lat/lon values of incidents
# ---------------------------------------------------------------------------------------------


def snap_points(row):
    global record_count
    record_count += 1  # Increment the counter

    #  Build the request url with parameters
    url = furl(path=rf"{url_base}route/GetRouteInfoByCoordinates",
               query_params={
               "xcoord": f"{row.get('Longitude', '')}",
               "ycoord": f"{row.get('Latitude', '')}",
               "snap_distance": 100,
               "return_multiple": False,
               "return_m": True,
               "return_keys": return_keys,
               "return_format": "json",
               "request_id": row.get('IncidentID', ''),
               "input_epsg": 4326,
               "output_epsg": 4326})

    print(f"Processing record {record_count}: {int(row.get('IncidentID'))}, {
          row.get('Longitude')}, {row.get('Latitude')}")

    # Send the request
    res = requests.get(url.tostr())

    if res.status_code == 200:
        res = json.loads(res.content.decode('utf-8'))
        if 'Route_Info' in res:
            route_info = res['Route_Info']
            route_info['IncidentID'] = int(row.get('IncidentID'))
            results.append(route_info)
        elif 'Info' in res:
            if 'request_id' in res:
                print(res['Info'], int(res['request_id']))
            else:
                print(res['Info'])
    else:
        print(res)

# Function to parse the 'POINT Z (x y z)' format


def parse_point_z(geometry):
    coords = geometry.replace('POINT Z (', '').replace(')', '').split()
    return Point(float(coords[0]), float(coords[1]), float(coords[2]))

# -------------------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------------------


if __name__ == '__main__':

    # Connect to SQLite database and read data into a pandas dataframe
    query = "SELECT IncidentID, Latitude, Longitude FROM collision_incidents;"
    df = pd.read_sql_query(query, conn)

    # Count the number of incidents to process
    number_of_rows = len(df)
    print(f"Number of rows to process: {number_of_rows}")

    # Create a Request ID
    df['Request_ID'] = df.index.astype(str)

    # Print the first 5 rows of the dataframe
    print(df)

    # Start the stopwatch / counter
    perf_counter_start = perf_counter()

    # Snap the points by sending requests to the API
    df.apply(snap_points, axis=1)

    # Stop the stopwatch / counter
    perf_counter_stop = perf_counter()

    # Put the results into a pandas dataframe
    df_results = pd.DataFrame(results)

    # Testing the results
    # print(df)
    # print(df_results)
    # print(df_results.columns)

    # Remove records where 'Geometry' is null
    df_results = df_results.dropna(subset=['Geometry'])

    # Filter rows where Geometry is null
    null_geometry_rows = df_results[df_results['Geometry'].isnull()]

    # Display the rows with null Geometry
    # print(null_geometry_rows)

    # Convert the 'Geometry' column from WKT to shapely geometries
    df_results['Geometry'] = df_results['Geometry'].apply(wkt.loads)

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(df_results, geometry='Geometry')

    # Set the coordinate reference system (CRS) if known; otherwise, use EPSG:4326 (WGS 84)
    gdf.set_crs(epsg=4326, inplace=True)

    # Save to GeoJSON
    geojson_path = os.path.join(
        cwd, 'data', 'api_clean_data', 'Roadway_Characteristics_API.geojson')
    gdf.to_file(geojson_path, driver='GeoJSON')

    # Convert the geometries to WKT format for storage in SQLite
    df_results['Geometry'] = df_results['Geometry'].apply(
        lambda geom: geom.wkt)

    # Ensure all columns have types that SQLite supports
    for col in df_results.columns:
        if df_results[col].dtype == object:
            df_results[col] = df_results[col].astype(str)

    # Write the df_results dataframe to the SQLite table
    df_results.to_sql('roadway_characteristics', conn,
                      if_exists='replace', index=False)

    # Establish a connection to the SQLite database
    conn = sqlite3.connect(database_path)

    # Write the dataframe to a table named 'Roadway_Characteristics_API'
    df_results.to_sql('Roadway_Characteristics_API', conn,
                      if_exists='replace', index=False)

    # Close the connection
    conn.close()
