import streamlit as st
import pandas as pd
from datetime import datetime
from src.data_loader import load_data

df = load_data('data/processed/Nassau-Candy-Distributor-Cleaned.pkl')
summary_df = load_data('data/processed/Summary-df.pkl')
summary_df2 = load_data('data/processed/Summary-df2.pkl')

st.set_page_config(
    page_title = 'Analysis Dashboard',
    page_icon = '📋',
    layout = 'wide',
    initial_sidebar_state = 'auto',
    menu_items = {}
)

col1, col2, col3 = st.columns([0.15, 0.75, 0.10])
with col1:
    st.image('logo.png', width = 'stretch')
with col2:
    st.title('Nassau Candy Distributor')
with col3:
    st.caption(f'Last Updated: {datetime.today().strftime("%d-%m-%Y %H:%M:%S")}')

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5, border = True)

filtered_df = df.copy() #For filters

with st.sidebar:
    with st.container():
        st.title('Filters')

        order_date_range = st.date_input(
            label = 'Select Order Date: ',
            value = (df['Order Date'].min(), df['Order Date'].max()),
            min_value = df['Order Date'].min(),
            max_value = df['Order Date'].max(),
            key = 'Order Date Range Filter'
        )

        if order_date_range and len(order_date_range) == 2:
            start_date = pd.to_datetime(order_date_range[0])
            end_date = pd.to_datetime(order_date_range[1])
            
            filtered_df = filtered_df[(filtered_df['Order Date'] >= start_date) & (filtered_df['Order Date'] <= end_date)]

        # ship_date_range = st.date_input(
        #     label = 'Select Ship Date: ',
        #     value = (df['Ship Date'].min(), df['Ship Date'].max()),
        #     min_value = df['Ship Date'].min(),
        #     max_value = df['Ship Date'].max(),
        #     key = 'Ship Date Range Filter'
        # )

        # if ship_date_range and len(ship_date_range) == 2:
        #     start_date = pd.to_datetime(ship_date_range[0])
        #     end_date = pd.to_datetime(ship_date_range[1])

        #     filtered_df = filtered_df[(filtered_df['Order Date'] >= start_date) & (filtered_df['Order Date'] <= end_date)]

        country_region = st.selectbox(
            'Select Country/Region: ',
            options = ['All'] + sorted(filtered_df['Country/Region'].unique()),
            index = 0,
            key = 'Country/Region Filter'
        )

        if country_region != 'All':
            filtered_df = filtered_df[filtered_df['Country/Region'] == country_region] 
            if filtered_df.empty:
                st.warning('No result(s) for applied filter!')

        state_province = st.selectbox(
            'Select State/Province: ',
            options = ['All'] + sorted(filtered_df['State/Province'].unique()),
            index = 0,
            disabled = True if country_region == 'All' else False,
            key = 'State/Province Filter'
            )

        if state_province != 'All':
            filtered_df = filtered_df[filtered_df['State/Province'] == state_province]
            if filtered_df.empty:
                st.warning('No result(s) for applied filter!')

        city = st.selectbox(
            label = 'Select City: ',
            options = ['All'] + sorted(filtered_df['City'].unique()),
            index = 0,
            disabled = True if country_region == 'All' else False,
            key = 'City Filter'
            )

        if city != 'All':
            filtered_df = filtered_df[filtered_df['City'] == city]
            if filtered_df.empty:
                st.warning('No result(s) for applied filter!')

        ship_mode = st.selectbox(
            label = 'Select Ship Mode: ',
            options = ['All'] + sorted(df['Ship Mode'].unique()),
            index = 0,
            key = 'Ship Mode Filter'
        )

        if ship_mode != 'All':
            filtered_df = filtered_df[filtered_df['Ship Mode'] == ship_mode]
            if filtered_df.empty:
                st.warning('No result(s) for applied filter!')

        # if country_region != 'All':
        #     filtered_df = filtered_df[filtered_df['Country/Region'] == country_region] 
        #     state_province = st.selectbox(
        #         'Select State/Province: ',
        #         options = ['All'] + sorted(filtered_df['State/Province'].unique()),
        #         index = 0,
        #         disabled = True if country_region == 'All' else False,
        #         key = 'State/Province Filter'
        #     )

        lead_time_slider = st.slider(
            label = 'Lead Time Selector',
            min_value = filtered_df['Shipping Lead Time'].min(),
            max_value = filtered_df['Shipping Lead Time'].max(),
            value = (filtered_df['Shipping Lead Time'].min(), filtered_df['Shipping Lead Time'].max()),
            key = 'Lead Time Slider'
        )

        if len(lead_time_slider) ==2:
            filtered_df = filtered_df[(filtered_df['Shipping Lead Time'] >= lead_time_slider[0]) & (filtered_df['Shipping Lead Time'] <= lead_time_slider[1])]


with kpi1:
    st.metric(
        label = 'Average Shipping Lead Time',
        value = filtered_df['Shipping Lead Time'].mean()
    )
with kpi2:
    st.metric(
        label = 'Average Shipping Lead Time',
        value = df['Shipping Lead Time'].mean()
    )

st.dataframe(filtered_df, hide_index = True)