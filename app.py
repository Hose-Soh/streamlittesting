#from collections.abc import Mapping
import json
import ee
#import geemap
import geemap.foliumap as geemap
import streamlit as st
import ipyleaflet
import folium
from folium.plugins import Draw
from streamlit_folium import folium_static
from shapely.geometry import Polygon, LineString, Point

# ______ GEE Authenthication ______

# _____ STREAMLIT _______

# Secrets
json_data = st.secrets["json_data"]
service_account = st.secrets["service_account"]

# Preparing values
json_object = json.loads(json_data, strict=False)
json_object = json.dumps(json_object)

# Authorising the app
credentials = ee.ServiceAccountCredentials(service_account, key_data=json_object)
ee.Initialize(credentials)
# Set page title
st.set_page_config(page_title='Streamlit Map Drawing Example')


m = geemap.Map()
# Display the map.
m.to_streamlit(height=600, responsive=True, scrolling=False)

# Get the drawn features from the map
drawn_features = m.draw_features
last_feature = m.draw_last_feature

geometry = None

if last_feature is not None and 'geometry' in last_feature.keys():
    geometry = last_feature['geometry']
    st.write("Last drawn feature's geometry:", geometry)
else:
    st.write("No features have been drawn yet.")

# Define a function to draw the feature on the map
def draw_feature_on_map(geometry):
    # Extract the coordinates based on the geometry type
    if geometry.type().getInfo() == 'Polygon':
    # For polygons, extract the exterior coordinates
        coords = geometry.coordinates().get(0).getInfo()
        for coord in coords:
            print(coord)
    elif geometry.type().getInfo() == 'LineString':
        # For lines, extract the coordinates
        coords = geometry.coordinates().getInfo()
        for coord in coords:
            print(coord)
    elif geometry.type().getInfo() == 'Point':
        # For points, extract the coordinates
        coords = geometry.coordinates().getInfo()
        print(coords)
    else:
        print("Unsupported geometry type.")

# Create a button to draw the feature
if st.button("Draw Feature"):
    draw_feature_on_map(geometry)


# Display the map.
m.to_streamlit(height=600, responsive=True, scrolling=False)