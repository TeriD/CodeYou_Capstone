# visualization.py
import os
import sqlite3
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


def create_collision_incidents_app():
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


# Run the app on a different port (e.g., 8051)
if __name__ == '__main__':
    app = create_collision_incidents_app()
    app.run_server(debug=True, port=8051)
