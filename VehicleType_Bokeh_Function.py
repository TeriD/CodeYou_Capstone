# visualization.py
import os
import sqlite3
import pandas as pd
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.palettes import Category20c
from bokeh.models import ColumnDataSource
from math import pi
import panel as pn


def create_vehicle_type_pie_chart():
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
