import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.figure_factory as ff
from matplotlib import pyplot as plt
import prepocessor, helper

# Olympics-themed color palette
OLYMPIC_COLORS = ["#0081C8", "#F4C300", "#00A651", "#EE334E", "#000000"]  # Blue, Yellow, Green, Red, Black

st.set_page_config(page_title="Olympics Analysis", layout="wide")

# Add sidebar background styling via markdown
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] > div:first-child {
        background-color: #f1f3f6;
        padding-top: 20px;
        border-right: 2px solid #d3d3d3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Simple Olympic Games Title
st.markdown("""
    <h2 style='text-align: center; color: #000;'>Olympic Games Data Analysis</h2>
    <hr style='border: 1px solid #CCCCCC;'>
""", unsafe_allow_html=True)

ath = pd.read_csv(r'athlete_events.csv.zip', compression = 'zip')
reg = pd.read_csv(r'noc_regions.csv')

df = prepocessor.preprocess(ath, reg)

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/512px-Olympic_rings_without_rims.svg.png", width=120)
st.sidebar.title("Olympics Dashboard")

user_menu = st.sidebar.radio(
    'Select an option',
    ("Medal's Analysis", 'Overall Analysis', 'Country-Wise Analysis', 'Athlete Wise Analysis')
)

if user_menu == "Medal's Analysis":
    st.sidebar.header("Medal Tally")
    years, country = helper.country(df)
    selected_year = st.sidebar.selectbox("Select Years", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    if selected_country == 'Overall' and selected_year == 'Overall':
        st.subheader('Olympics Performance Till 2016')
    elif selected_country != 'Overall' and selected_year == 'Overall':
        st.subheader(f"{selected_country} Performance Overall")
    elif selected_country == 'Overall' and selected_year != 'Overall':
        st.subheader(f"Overall Olympics In {selected_year}")
    else:
        st.subheader(f"{selected_country} Performance in {selected_year}")

    medal_tally = helper.fetch_medal_tally(selected_year, selected_country, df)
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    st.subheader('Top Statistics')
    edition = df.Year.unique().shape[0] - 1
    cities = df.City.unique().shape[0]
    sports = df.Sport.unique().shape[0]
    events = df.Event.unique().shape[0]
    athelets = df.Name.unique().shape[0]
    country = df.region.unique().shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Editions", edition)
    col2.metric("Host Cities", cities)
    col3.metric("Sports", sports)

    col1, col2, col3 = st.columns(3)
    col1.metric("Events", events)
    col2.metric("Athletes", athelets)
    col3.metric("Countries", country)

    nation_over_time = helper.data_time(df, 'region')
    fig = px.line(nation_over_time, x='Edition', y='region', markers=True, title="Participating Nations Over Time")
    fig.update_traces(line=dict(color=OLYMPIC_COLORS[0]))
    st.plotly_chart(fig)

    events_over_time = helper.data_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event', markers=True, title="Events Over Time")
    fig.update_traces(line=dict(color=OLYMPIC_COLORS[1]))
    st.plotly_chart(fig)

    athelets_over_time = helper.data_time(df, 'Name')
    fig = px.line(athelets_over_time, x='Edition', y='Name', markers=True, title="Athletes Over Time")
    fig.update_traces(line=dict(color=OLYMPIC_COLORS[2]))
    st.plotly_chart(fig)

    st.subheader('Events Over Time (Every Sport)')
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    heatmap_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(heatmap_data, annot=True, ax=ax, cmap="YlGnBu", linewidths=0.5)
    st.pyplot(fig)

    st.subheader('Most Successful Athletes')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')
    selected = st.selectbox('Select Sports', sports_list)
    x = helper.most_successful_ath(df, selected)
    st.table(x)

if user_menu == 'Country-Wise Analysis':
    st.sidebar.subheader('Country Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected = st.sidebar.selectbox('Select Country', country_list)

    country_df = helper.country_wise_medal(df, selected)
    fig = px.line(country_df, x='Year', y='Medal', markers=True, title=f"{selected} Medal Tally Over The Years")
    fig.update_traces(line=dict(color=OLYMPIC_COLORS[3]))
    st.plotly_chart(fig)

    st.subheader(f"{selected} Excels in the Following Sports")
    pt = helper.country_medal_heatmap(df, selected)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt, annot=True, ax=ax, cmap="YlGnBu", linewidths=0.5)
    st.pyplot(fig)

    st.subheader(f"Top 10 Athletes from {selected}")
    pt = helper.most_success_ath_count_wise(df, selected)
    st.table(pt)

if user_menu == "Athlete Wise Analysis":
    st.subheader("Age Distribution")
    athelte_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athelte_df['Age'].dropna()
    x2 = athelte_df[athelte_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelte_df[athelte_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelte_df[athelte_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ["All Athletes", 'Gold', 'Silver', 'Bronze'], show_rug=False, show_hist=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    st.subheader('Height vs Weight Comparison')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')
    selected = st.selectbox('Select Sport', sports_list)

    temp_df = helper.weight_v_height(df, selected)
    fig, ax = plt.subplots()
    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=70, ax=ax)
    st.pyplot(fig)

    st.subheader('Male vs Female Participation Over Years')
    f = helper.men_v_women(df)
    fig = px.line(f, x='Year', y=['Male', 'Female'], markers=True)
    fig.update_traces(line=dict(width=2))
    st.plotly_chart(fig)
