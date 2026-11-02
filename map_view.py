import json
import pandas as pd
import plotly.express as px
from region_config import REGIONS, UNION_TERRITORIES

with open("india_states_merged.geojson", encoding="utf-8") as f:
    INDIA_GEOJSON = json.load(f)

COLORS = {
    "Movies available": "#B58A8D",
    "Coming soon": "#E9DFD2",
    "Union Territory": "#D9CDBE",
    "Selected": "#6D2638",
}

def region_status(name):
    if REGIONS[name]["industry"]:
        return "Movies available"
    if name in UNION_TERRITORIES:
        return "Union Territory"
    return "Coming soon"


def build_map(selected=None):
    df = pd.DataFrame({"region": list(REGIONS.keys())})
    df["status"] = df["region"].apply(region_status)
    if selected:
        df.loc[df["region"] == selected, "status"] = "Selected"

    fig = px.choropleth(
        df,
        geojson=INDIA_GEOJSON,
        locations="region",
        featureidkey="properties.st_nm",
        color="status",
        color_discrete_map=COLORS,
        hover_name="region",
        hover_data={"region": False, "status": False},
    )
    fig.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
    fig.update_traces(marker_line_color="#8A7B70", marker_line_width=0.6)
    fig.update_layout(
        paper_bgcolor="#F5F0E7",
        margin=dict(l=0, r=0, t=0, b=0),
        height=650,
        legend=dict(title="", font=dict(color="#302621")),        
    )
    return fig