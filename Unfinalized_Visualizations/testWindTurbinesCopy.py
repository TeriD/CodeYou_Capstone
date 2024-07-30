import holoviews as hv
import os
import panel as pn
import pandas as pd
import geopandas as gpd

pn.extension('vizzu', 'tabulator', design='material', template='material')

# Load GeoJSON file
cwd = os.getcwd()
geojson_path = f'{cwd}/data/api_clean_data/Roadway_Characteristics_API.geojson'
geo_data = gpd.read_file(geojson_path)

# Convert GeoDataFrame to DataFrame for use in the template
geo_data['geometry'] = geo_data['geometry'].apply(lambda x: x.wkt)
geo_df = pd.DataFrame(geo_data)


def data(df, groupby, quant):
    if quant == 'Count':
        return df.value_counts(groupby).to_frame(name='Count').sort_index().reset_index().iloc[:50]
    else:
        return df.groupby(groupby)[quant].sum().reset_index().iloc[:50]


def config(chart_type, groupby, quant):
    if chart_type == 'Bubble Chart':
        return {
            "channels": {
                "x": None,
                "y": None,
                "color": groupby,
                "label": groupby,
                "size": quant
            },
            'geometry': 'circle'
        }
    else:
        return {
            "channels": {
                "x": groupby,
                "y": quant,
                "color": None,
                "label": None,
                "size": None
            },
            'geometry': 'rectangle'
        }


ls = hv.link_selections.instance()

geo = ls(geo_df.hvplot.points(
    'longitude', 'latitude', xaxis=None, yaxis=None, rasterize=True,
    tiles='CartoLight', responsive=True, dynspread=True,
    height=500, cnorm='log', cmap='plasma', xlim=(-14000000, -8000000),
    ylim=(3000000, 6500000)
))

groupby = pn.widgets.RadioButtonGroup(
    options={'COUNTY': 'County_Name', 'Year': 'year', 'Manufacturer': 'manufacturer'}, align='center'
)
chart_type = pn.widgets.RadioButtonGroup(
    options=['Bar Chart', 'Bubble Chart'], align='center'
)
quant = pn.widgets.RadioButtonGroup(
    options={'Count': 'Count', 'Capacity': 'capacity'}, align='center'
)
lsdata = ls.selection_param(geo_df)

vizzu = pn.pane.Vizzu(
    pn.bind(data, lsdata, groupby, quant),
    config=pn.bind(config, chart_type, groupby, quant),
    column_types={'year': 'dimension'},
    style={
        "plot": {
            "xAxis": {
                "label": {
                    "angle": "-45deg"
                }
            }
        }
    },
    sizing_mode='stretch_both'
)


def format_df(df):
    df = df[['county_name', 'county', 'name',
             'year', 'manufacturer', 'capacity']]
    return df.rename(
        columns={col: col.title() for col in df.columns}
    )


table = pn.widgets.Tabulator(
    pn.bind(format_df, lsdata), page_size=8, pagination='remote',
    show_index=False,
)

pn.Column(
    pn.Row(quant, "# by", groupby, "# as a",
           chart_type).servable(area='header'),
    pn.Column(
        pn.Row(geo, table),
        vizzu, min_height=1000,
        sizing_mode='stretch_both'
    ).servable(title='GeoJSON Data Visualization')
)
