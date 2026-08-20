from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_data

DATA_PATH = "data/processed/Nassau-Candy-Distributor-Cleaned.pkl"
DELAY_QUANTILE = 0.75
US_STATE_CODES = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", 
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", 
    "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", 
    "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", 
    "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", 
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", 
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", 
    "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", 
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", 
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
}


@st.cache_data(show_spinner=False)
def get_data() -> pd.DataFrame:
    data = load_data(DATA_PATH)
    if data is None:
        raise FileNotFoundError(DATA_PATH)
    data = data.copy()
    for column in ("Order Date", "Ship Date"):
        data[column] = pd.to_datetime(data[column], errors="coerce")
    data["Shipping Lead Time"] = pd.to_numeric(data["Shipping Lead Time"], errors="coerce")
    data["Factory to Customer State"] = (
        data["Factory Name"].astype(str) + " → " + data["State/Province"].astype(str)
    )
    data["Factory to Customer Region"] = (
        data["Factory Name"].astype(str) + " → " + data["Country/Region"].astype(str)
    )
    return data.dropna(subset=["Order Date", "Ship Date", "Shipping Lead Time"]).query("`Shipping Lead Time` >= 0")


def route_summary(data: pd.DataFrame, route_column: str) -> pd.DataFrame:
    """Calculate route KPIs; 100 is the fastest route in the current filter context."""
    threshold = data["Shipping Lead Time"].quantile(DELAY_QUANTILE)
    summary = data.groupby(route_column, dropna=False).agg(
        Route_Volume=("Order ID", "nunique"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Lead_Time_Variability=("Shipping Lead Time", "std"),
        Delay_Frequency=("Shipping Lead Time", lambda values: (values > threshold).mean() * 100),
    ).reset_index()
    summary["Lead_Time_Variability"] = summary["Lead_Time_Variability"].fillna(0)
    spread = summary["Avg_Lead_Time"].max() - summary["Avg_Lead_Time"].min()
    summary["Route_Efficiency_Score"] = 100 if spread == 0 else (
        100 * (summary["Avg_Lead_Time"].max() - summary["Avg_Lead_Time"]) / spread
    ).round(1)
    return summary.sort_values(["Route_Efficiency_Score", "Route_Volume"], ascending=[False, False])


def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    filtered = data.copy()
    with st.sidebar:
        st.header("Filters")
        date_range = st.date_input("Order date range", value=(data["Order Date"].min().date(), data["Order Date"].max().date()), min_value=data["Order Date"].min().date(), max_value=data["Order Date"].max().date())
        if len(date_range) == 2:
            filtered = filtered[filtered["Order Date"].between(*map(pd.Timestamp, date_range))]
        for label, column in (("Country / region", "Country/Region"), ("State / province", "State/Province"), ("Ship mode", "Ship Mode")):
            selected = st.selectbox(label, ["All"] + sorted(filtered[column].dropna().astype(str).unique().tolist()))
            if selected != "All":
                filtered = filtered[filtered[column].astype(str) == selected]
        if filtered.empty:
            st.info("No shipments match the selected filters.")
            return filtered
        low, high = map(int, (filtered["Shipping Lead Time"].min(), filtered["Shipping Lead Time"].max()))
        lead_range = st.slider("Lead-time range (days)", low, high, (low, high))
        filtered = filtered[filtered["Shipping Lead Time"].between(*lead_range)]
    return filtered


st.set_page_config(page_title="Nassau Candy Route Efficiency", page_icon="🍬", layout="wide")
st.title("Factory-to-Customer Shipping Route Efficiency")
title_col, logo_col = st.columns([4, 1])
with title_col:
    st.caption("Nassau Candy Distributor | Live logistics decision support")
with logo_col:
    if Path("logo.png").exists():
        st.image("logo.png", use_container_width=True)
st.caption(f"Dashboard refreshed: {datetime.now():%d %b %Y, %H:%M}")

try:
    df = get_data()
except (FileNotFoundError, KeyError) as error:
    st.error(f"Unable to prepare the dashboard data: {error}")
    st.stop()
filtered_df = apply_filters(df)
if filtered_df.empty:
    st.warning("Adjust the filters to view analytics.")
    st.stop()

state_summary = route_summary(filtered_df, "State/Province")
route_state_summary = route_summary(filtered_df, "Factory to Customer State")
delay_threshold = filtered_df["Shipping Lead Time"].quantile(DELAY_QUANTILE)
kpis = st.columns(5)
kpis[0].metric("Average lead time", f"{filtered_df['Shipping Lead Time'].mean():.1f} days")
kpis[1].metric("Route volume", f"{filtered_df['Order ID'].nunique():,} orders")
kpis[2].metric("Delayed shipments", f"{(filtered_df['Shipping Lead Time'] > delay_threshold).sum():,}")
kpis[3].metric("Fastest shipment", f"{filtered_df['Shipping Lead Time'].min():.0f} days")
kpis[4].metric("Slowest shipment", f"{filtered_df['Shipping Lead Time'].max():.0f} days")
st.caption(f"Delayed shipments exceed the current 75th-percentile lead-time threshold ({delay_threshold:.1f} days).")

overview_tab, geography_tab, mode_tab, drilldown_tab = st.tabs(["Route efficiency overview", "Geographic bottlenecks", "Ship-mode comparison", "Route drill-down"])
with overview_tab:
    left, right = st.columns(2)
    with left:
        slowest = route_state_summary.sort_values("Avg_Lead_Time", ascending=False).head(15)
        fig = px.bar(slowest, x="Avg_Lead_Time", y="Factory to Customer State", orientation="h", color="Route_Efficiency_Score", color_continuous_scale="RdYlGn", range_color=[0, 100], labels={"Avg_Lead_Time": "Average lead time (days)", "Route_Efficiency_Score": "Efficiency score"}, title="Average lead time by route (top 15 slowest)")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Route performance leaderboard")
        st.dataframe(route_state_summary.head(10)[["Factory to Customer State", "Route_Efficiency_Score", "Avg_Lead_Time", "Route_Volume", "Delay_Frequency"]], hide_index=True, use_container_width=True)
        st.subheader("Least efficient routes")
        st.dataframe(route_state_summary.tail(10).sort_values("Route_Efficiency_Score")[["Factory to Customer State", "Route_Efficiency_Score", "Avg_Lead_Time", "Route_Volume", "Delay_Frequency"]], hide_index=True, use_container_width=True)
with geography_tab:
    map_data = state_summary.copy()
    map_data["State Code"] = map_data["State/Province"].map(US_STATE_CODES)
    map_data = map_data.dropna(subset=["State Code"])
    if not map_data.empty:
        fig = px.choropleth(map_data, locations="State Code", locationmode="USA-states", scope="usa", color="Route_Efficiency_Score", hover_name="State/Province", hover_data={"Avg_Lead_Time": ":.1f", "Route_Volume": True, "Delay_Frequency": ":.1f", "State Code": False}, color_continuous_scale="RdYlGn", range_color=[0, 100], labels={"Route_Efficiency_Score": "Efficiency score"}, title="US shipping efficiency by customer state")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No mappable US state records are available for the current filters.")
    fig = px.scatter(state_summary, x="Route_Volume", y="Avg_Lead_Time", size="Delay_Frequency", color="Route_Efficiency_Score", hover_name="State/Province", color_continuous_scale="RdYlGn", range_color=[0, 100], labels={"Route_Volume": "Shipment volume", "Avg_Lead_Time": "Average lead time (days)"}, title="Regional bottleneck analysis: high volume and high lead time indicate priority areas")
    st.plotly_chart(fig, use_container_width=True)
with mode_tab:
    mode_summary = filtered_df.groupby("Ship Mode").agg(Shipments=("Order ID", "nunique"), Avg_Lead_Time=("Shipping Lead Time", "mean"), Median_Lead_Time=("Shipping Lead Time", "median"), Avg_Cost=("Cost", "mean")).reset_index()
    fig = px.bar(mode_summary.sort_values("Avg_Lead_Time"), x="Ship Mode", y="Avg_Lead_Time", text_auto=".1f", color="Avg_Cost", color_continuous_scale="Blues", labels={"Avg_Lead_Time": "Average lead time (days)", "Avg_Cost": "Average cost"}, title="Lead-time and cost comparison by ship mode")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(mode_summary, hide_index=True, use_container_width=True)
with drilldown_tab:
    selected_state = st.selectbox("Select a state / province", sorted(filtered_df["State/Province"].dropna().unique()))
    records = filtered_df[filtered_df["State/Province"] == selected_state].sort_values("Order Date")
    fig = px.scatter(records, x="Order Date", y="Shipping Lead Time", color="Ship Mode", size="Units", hover_data=["Order ID", "Product Name", "City", "Ship Date", "Factory Name"], title=f"Order-level shipment timeline: {selected_state}", labels={"Shipping Lead Time": "Lead time (days)"})
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(records[["Order ID", "Order Date", "Ship Date", "Factory Name", "City", "Ship Mode", "Product Name", "Units", "Shipping Lead Time"]], hide_index=True, use_container_width=True)
