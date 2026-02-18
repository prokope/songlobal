import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_theme import st_theme
import folium
from streamlit_folium import st_folium
import geopandas as gpd

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.set_page_config(page_title='Songlobal', page_icon=':musical_note:', layout='wide')
st.markdown('<h1 style="font-family: Inter; font-size: 29px;">Songlobal</h1>', unsafe_allow_html=True, text_alignment='center')

theme = st_theme()

theme_color = 'black'
if theme and theme['base'] == 'dark':
    theme_color = 'white'

elif theme['base'] == 'light':
    theme_color = 'black'

col1, col2 = st.columns(2, border=0)

with col1:
    col1.title('Top Artists', text_alignment='center')
    c1 = col1.container(height=400, horizontal_alignment='center')

    with c1:
        subc1 = c1.container(border=0, width=500)
        subcol1, subcol2 = subc1.columns(2)

        with subcol1:
            limit = st.selectbox( 'View', ('Top 10', 'Top 50', 'Top 100'))
        with subcol2:
            rankMethod = st.selectbox( 'By', ('Popularity'))

        with subc1:
            artists_metrics = pd.read_csv('data/artists_metrics.csv')
            artists_metrics = artists_metrics.iloc[:int(limit[4:])]
            st.bar_chart(artists_metrics, x='artist_name', y='artist_popularity', horizontal=True, sort=False, y_label=' ', x_label='', width='stretch')


    col1.title('Top Genres', text_alignment='center')
    c2 = col1.container(border=True, horizontal_alignment='center')

    with c2:
        subc2 = c2.container(border=0, width=500)

        with subc2:
            limit = st.selectbox('By', ('Top 100 artists'))
            top_100_artists_labels = pd.read_csv('data/top_100_artists_labels.csv')
            top_100_artists_labels = pd.Series(data=(np.array(top_100_artists_labels['count'])), index=(top_100_artists_labels['genre'].to_list()))

            fig, ax = plt.subplots()
            fig.patch.set_facecolor('none')
            ax.patch.set_facecolor('none')

            labels = top_100_artists_labels.index
            percent = top_100_artists_labels

            explode = [0.2 for label in top_100_artists_labels.index]

            wedges, texts, autotexts = ax.pie(
                percent,  # -> Values
                labels=labels,  # -> Labels (Series index)
                labeldistance=1.1,  # -> Label distance from chart
                explode=explode,  # -> Distance between chart pieces
                autopct='%1.1f%%',  # -> Auto-calculating the percentage
                radius=1.7,  # -> Increasing circle radius
                wedgeprops=dict(width=0.7),  # -> Turning pie into a donut (adding a circle inside it)
                pctdistance=0.75  # -> Adjusting the percentage distance from chart
            )

            # Just percentages
            for t in autotexts:
                t.set_color('white')
                t.set_fontsize(10)
                t.set_fontweight('bold')

            for text in texts:
                text.set_color(theme_color)

            plt.title('Top genres on top 100 artists', color=theme_color, pad=90)

            st.pyplot(fig)


with col2:
    col2.title('Top Artists by Country', text_alignment='center')

    c3 = col2.container(border=True, height=400, horizontal_alignment='center')

    with c3:
        subc3 = c3.container(border=0, width=500)

        with subc3:
            """
            artists_nationalities = pd.read_csv('data/artists_nationalities.csv')
            artists_by_country = artists_nationalities.value_counts()
            gdf = gpd.read_file('data/ne_10m_admin_0_map_units.json')
            gdf[(gdf['ADMIN'] == 'United Kingdom')] = gdf[(gdf['ADMIN'] == 'United Kingdom')].replace('-99', 'GB')
            gdf[(gdf['ADMIN'] == 'South Korea')] = gdf[(gdf['ADMIN'] == 'South Korea')].replace('-99', 'KR')
            gdf[(gdf['ADMIN'] == 'Netherlands')] = gdf[(gdf['ADMIN'] == 'Netherlands')].replace('-99', 'NL')
            gdf[(gdf['ADMIN'] == 'Belgium')] = gdf[(gdf['ADMIN'] == 'Belgium')].replace('-99', 'BE')
            gdf.set_index('ISO_A2', inplace=True)
            gdf['top_artists'] = gdf.index.map(artists_by_country)
            gdf['top_artists'] = gdf['top_artists'].fillna(0)
            gdf['top_artists'] = gdf['top_artists'].astype(int)
            gdf = gdf.drop('AQ')

            m = folium.Map(location=[0,0], zoom_start=2)

            folium.GeoJson(gdf).add_to(m)
            st_folium(m, width=800, height=600)
            """



