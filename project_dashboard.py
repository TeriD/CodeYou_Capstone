# main.py
from incidentsByDistrict_Year_Function import create_collision_incidents_app
from VehicleType_Bokeh_Function import create_vehicle_type_pie_chart
from HumanFactors_Functions import generate_top_factors_bar_chart
import panel as pn
from jupyter_dash import JupyterDash


def main():
    pn.extension()

    collision_incidents_app = create_collision_incidents_app()
    vehicle_type_pie_chart = create_vehicle_type_pie_chart()
    bar_chart_pane = generate_top_factors_bar_chart()

    collision_incidents_dash = JupyterDash.from_dash(collision_incidents_app)
    collision_incidents_dash.run_server(mode='inline')

    layout = pn.Column(
        pn.pane.Markdown(
            "# Collision Incidents and Vehicle Types Visualization"),
        pn.Row(
            pn.Column(
                pn.pane.Markdown(
                    "## Collision Incidents by District and Year"),
                collision_incidents_dash
            ),
            pn.Column(
                pn.pane.Markdown("## Vehicle Types Involved in Collisions"),
                vehicle_type_pie_chart
            )
        ),
        pn.pane.Markdown("## Top Human Factors Bar Chart"),
        bar_chart_pane
    )

    layout.show()


if __name__ == '__main__':
    main()
