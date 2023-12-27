import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import altair as alt

st.title('GitHub Repository Analysis')
st.header('by Naama Bejerano')

# Goals and Objectives Section
st.header('Goals and Notes:')
st.markdown("""
- Analyze GitHub repository data to highlight interesting information from the data.
- I used the version 2 dataset from the [Kaggle GitHub Dataset](https://www.kaggle.com/datasets/nikhil25803/github-dataset/data?select=repository_data.csv) (repository_data.csv).
    - * Since the dataset is so large the data processing through streamlit was very slow on my computer, I wrote python scripts to process the data into csv files and displayed the csv files using streamlit. The corresponsding python script for each graph is linked.
""")

# Data Cleaning Section
st.header('Data Cleaning:')
st.markdown("""
- Ensure the dataset is valid, make note of which rows / cells to exclude.
- Count unique rows to check for repetition (none found), count number of empty cells, range of numeric values and date.
- Key findings:
    - The data is from 1/1/2009 until 1/21/2023, when looking for paterns based on months, years, or seasons exclude data from 2023.
    - 47 percent of the license column is empty (1378200 cells), observations about licenses only pertain to less than half of the data.
- [Data Cleaning Code](https://drive.google.com/file/d/1RoIzXc8o3G_Uht6wBzg6TdrCkg2aBdON/view?usp=sharing)
""")

st.header('Top 5 Most Popular Repositories Overall')
st.markdown("""
Popularity is measured by a sum across the value associated with stars_count,forks_count,watchers,pull_requests, and commit_count.
""")
# Read the CSV file
file_path = '/names_most_pop.csv'
top_repositories = pd.read_csv(file_path)

# Create a horizontal bar chart using Altair
chart = alt.Chart(top_repositories).mark_bar(size=15).encode(
    x=alt.X('overall_popularity:Q', title='Overall Popularity'),
    y=alt.Y('name:N', sort='-x', title='Repository Name', axis=alt.Axis(labelPadding=8)),
    color='name:N',
    tooltip=['name:N', alt.Tooltip('overall_popularity:Q')]
).properties(
    title='Top Repositories by Overall Popularity',
    width=600, 
    height=300  
)

# Configure axis and disable legend
chart = chart.configure_axis(titleFontSize=14, labelFontSize=10)
chart = chart.configure_legend(disable=True)

# Display the chart
chart

st.markdown('<span style="font-size:15px;"> The average popularity of a repository in the data set is 742.765680095382.</span>', unsafe_allow_html=True)
st.markdown('<span style="font-size:15px;"> __Key Finding__: The most popular repository is significantly more popular than those that follow, and the average overall is much below.</span>', unsafe_allow_html=True)

st.header('Trends based on Programming Language:')
st.markdown("""
- About 7.5 percent of the rows are not included since the primary_language column is empty.
""")

st.markdown("### [Average Popularity by Programming Language](https://drive.google.com/file/d/1O6yax1ct8qw2zJ_rVd4yl7QBd3bY3JaA/view?usp=sharing)")

# Specify the path to your CSV file
average_popularity_by_language_path = '/Users/naama/Desktop/Beacon/average_popularity_by_language.csv'

# Read the CSV file into a pandas DataFrame
pop_language_df = pd.read_csv(average_popularity_by_language_path)

# Sort the DataFrame by overall_popularity in descending order
pop_language_df = pop_language_df.sort_values(by='overall_popularity', ascending=False)

# Create a bar chart using Altair
chart = alt.Chart(pop_language_df).mark_bar().encode(
    x=alt.X('primary_language:N', sort='-y', title='Programming Languages'),
    y=alt.Y('overall_popularity:Q', title='Average Popularity')
)

# Display the chart using Streamlit
st.altair_chart(chart, use_container_width=True)

st.markdown('<span style="font-size:15px;"> __Key Finding__: The most popular repositories have a primary languages commonly associated with documentation.</span>', unsafe_allow_html=True)
st.markdown('<span style="font-size:12px;"> Popularity in this case is measured by a sum across the value associated with stars_count,forks_count,watchers,pull_requests, and commit_count.</span>', unsafe_allow_html=True)
st.markdown('<span style="font-size:12px;"> *Rows where any of the above values are empty are excluded (only commit_count column has empty cells these are .065 percent of the data).</span>', unsafe_allow_html=True)


st.markdown("### [Percent of Repositories Created by Language Over Time](https://drive.google.com/file/d/1Cpks-MrerlyeKUa888Fgvlc8aj9rGqmz/view?usp=sharing)")

top_lang_over_time = '/Users/naama/Desktop/Beacon/top_lang_pop_over_time.csv'
top_lang_over_time_df = pd.read_csv(top_lang_over_time)

# Melt the DataFrame to make it suitable for Altair
df_melted = pd.melt(top_lang_over_time_df, id_vars=['created_year'], var_name='Programming Language', value_name='Value')

# Create a line chart using Altair
chart = alt.Chart(df_melted).mark_line().encode(
    x=alt.X('created_year:N', title='Year'),
    y=alt.Y('Value:Q', title='Percent of Repositories Created'),
    color='Programming Language:N'
).properties(
    width=600,
    height=400
)

# Display the chart using Streamlit
st.altair_chart(chart, use_container_width=True)

st.markdown('<span style="font-size:15px;"> __Key Finding__: There is a clear trend in the fall in the popularity of Ruby from 2009 and the extreme rise in popularity of Python in recent years.</span>', unsafe_allow_html=True)
st.markdown('<span style="font-size:12px;"> * I chose to highlight 5 languages that were the most used which showed interesting trends.</span>', unsafe_allow_html=True)

st.header('Trends based on Time:')
st.markdown("""
- Since the data set includes up to 1/21/2023, when looking at larger trends over years or months the data from 2023 is excluded.
""")

st.markdown("### [Number of Repositories Created Over Time](https://drive.google.com/file/d/1ek3YMuSprsIheXT-93jpZ1vavjrjabXx/view?usp=sharing)")

# Specify the path to your CSV file
data_path = '/Users/naama/Desktop/Beacon/repositories_by_year.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(data_path)

# Create an area chart using Altair
chart = alt.Chart(df).mark_area(
    interpolate='linear',
    line=True,
    color='steelblue',
    opacity=0.8
).encode(
    x=alt.X('created_year:N', title='Year'),
    y=alt.Y('0:Q', title='# Repositories Created')
).properties(
    width=600,
    height=400
)

# Display the chart using Streamlit
st.altair_chart(chart, use_container_width=True)

st.markdown('<span style="font-size:15px;"> __Key Finding__: There is a steady increase since 2009, with a relatively consistent rate, the peak appears to be in 2020. This can be explained by the Covid 19 epidemic which closed people in their homes and was most disruptive during 2020 offering an explaination as to why there was a stark increase and since 2020 there has been a decrease.</span>', unsafe_allow_html=True)

st.markdown("### [Average Number of Repositories Created Per Season](https://drive.google.com/file/d/12Tga-F2_DcStsfBuJ_t6YfCAoSsnUzxz/view?usp=sharing)")
# Specify the path to your CSV file
data_path = '/Users/naama/Desktop/Beacon/average_repositories_by_season.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(data_path)

# Create a bar chart using Altair with a trend line
chart = alt.Chart(df).mark_bar(size=40).encode(
    x='Season:N',
    y=alt.Y('Average Repositories:Q', scale=alt.Scale(type='log', base=2)),
    tooltip=['Season:N', 'Average Repositories:Q']
).properties(
    title='Log Base 2 Transformed Average Repositories by Season',
    width=400,
    height=500
)

# Add a trend line connecting the bars
trendline = chart.mark_line(color='blue').encode(
    x='Season:N',
    y='Average Repositories:Q'
)

# Overlay the trend line on the bar chart
final_chart = chart + trendline

# Display the chart using Streamlit
st.altair_chart(final_chart, use_container_width=True)

st.markdown('<span style="font-size:15px;"> __Key Finding__: The most repositories are created in the spring and the least are created in the winter, there is no information provided on dates in which users interact with the repositroy this would be itneresting to know as well.</span>', unsafe_allow_html=True)

# Further Analysis
st.header('Further Analysis:')
st.markdown("""
- The dataset contains a large amount of information and there are many more analyses that can be such as:
    - Comparisons between version 1 dataset and version 2 dataset.
    - Analysis of the licenses:
        - Anlysis of popularity of repository based on the license.
        - Amount of interactivity a repository recieves (sum of commit_count and pull_count) based on the license.
""")

# Failed Analyses
st.header('Anlyses Conducted not Highlighted:')
st.markdown("""
- These analyses were conducted but did not provided valuable insight to the same extent that the highlight data above did. They are included here for reference.
""")

st.markdown("### [Average Number of Repositories Created by Month](https://drive.google.com/file/d/1ro52B3Eyf1I4UDG-fDYD5gKhE16WAKKP/view?usp=sharing)")
# Read the CSV file
csv_file_path = '/Users/naama/Desktop/Beacon/avg_rep_month.csv'
result_df = pd.read_csv(csv_file_path)

# Create a vertical bar chart
chart = alt.Chart(result_df).mark_bar().encode(
    x='Month:N',
    y='Average Repositories:Q',
    tooltip=['Month:N', 'Average Repositories:Q']
).properties(
    title='Average Repositories Created Per Month',
    width=600,
    height=400
)

st.altair_chart(chart, use_container_width=True)
st.markdown('<span style="font-size:15px;"> The graph of repositories created by season provided more clear insight into trends in the data.</span>', unsafe_allow_html=True)

st.markdown("### [Popularity by Number of Languages Used per Repository](https://drive.google.com/file/d/1u90Pqb_mi_ufWC_2JCOq0BAJ7v5TgpcB/view?usp=sharing)")

# Display the plot in Streamlit
st.image('/Users/naama/Desktop/Beacon/Screen Shot 2023-12-23 at 10.09.36 PM.png', use_column_width=True)


st.markdown('<span style="font-size:15px;"> The data processing was too dense to be processed in streamlit to create the plot.</span>', unsafe_allow_html=True)

