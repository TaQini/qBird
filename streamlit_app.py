import folium
import streamlit as st

from streamlit_folium import st_folium

m = folium.Map(location=[39.97364, 116.36218], zoom_start=16)

f = open('./test.db','r')
merge = eval(f.read())
f.close()

print('opening database...')

for spp in merge:
    for obs in merge[spp]:
        print(obs)
        comName = spp
        obsDt = obs[0]
        howManyStr = obs[1]
        loc = [obs[2],obs[3]]
        locName = obs[4]
        folium.Marker(
            loc, popup=f"{obsDt}\n{locName}", tooltip=comName
        ).add_to(m)

# call to render Folium map in Streamlit
# st_data = st_folium(m)
st_data = st_folium(m, width=1200)
