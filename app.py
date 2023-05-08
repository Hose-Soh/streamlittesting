#from collections.abc import Mapping
import json
import ee
import geemap
#import geemap.foliumap as geemap
import streamlit as st
import ipyleaflet
import folium
from folium.plugins import Draw
from streamlit_folium import folium_static
from shapely.geometry import Polygon

# Data from the downloaded JSON file
json_data = '''
{
  "type": "service_account",
  "project_id": "curious-domain-385602",
  "private_key_id": "1f2c837e27d3d81c85f94ca6e7ddcb34c3085d88",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDFzdkyiJJYgObt\nsbpP8dhHFHhfTE3L37R9P8OMMxA5vliM1jqdt6NJkFPFHRf57z7WP0GnVe36Gq3B\nrkfky7C1y0aefqxCaxSiddoMsu0XrKWtusMx5Y9dfgIFr2wulEgnzxhXdDmNr6P3\nQfb9A43a3eu2GbAP3B2TWPNhsSb/Vf1+nGI39HFABdNa7u8hi3lu0i9Unvi+yhbI\n6/KAiPMFleEWj3mZkCin4XRSrVQACFEYiFKsqtYWDg68PknwaXM+dXEeLqqAjHaE\nn8iB6mJs6B4U80FB0fuIdl9b730s5v2b4Y84EdZA+rapsxCp2h0/B9TB2pTXRkKS\ngmhBdFi3AgMBAAECggEAJp9ZfAz/qklNDfdofiimRsa/9Delbxv4lYYoTA1Ca0v3\n5VQFMPuE5h3IxZG3N0WYOuQyERbttyqTZ+B8SDffgre0y8jHINbguhIR5+3d7oP2\n+7OeXnVI54PtqCeHE5c/eYpt4dGfVUOI3AQk0mVpwuUXG8DrSEV9/uHc7+PTzgIn\nighVkKoxUR65kiKEzegyIZKp7uNh4u9+0q/C/jIRFGpURFrdN6i8o+SXzCNPBXQD\noApwTPDOnKEMXiWjTUgRfmocQFT+3xkFrDkLlrmshArSVg0xpaQlmzaustVeUbYY\nAwLkB0ljwZr7/ugxl76FGqK9Mg5iI3luM5XLbrHfaQKBgQD31M1IbhMI1GMl10ih\nZk2OCoo2kkYxhiHc8aAO1oy81SC68dN9O/GSsLU3PT7ODU/VlT2E4r5eosAquWee\n4evxP869LsTvspjiO06576CF4+VmAoGURSWgCzc+By/1Dpy2EZ+mao28AyYbRhTe\nDGEPV+O/m53nYj7MqMKImpW4TwKBgQDMUuryRx6dcE5Pl2SqunOfmHrBZyphSX59\nRprtZcPuR60AKNAUcRsQWKy//CH4GBcTp0LBPNzr2n/Qe1n0gh/d3sU3yEwgpoXY\nBR+lrWaTEh8RuBa3he9XOxpNSGIpwswAHlHkmR0DcgUbtNYc7jFT5h+x3caPtjxP\nwJksNoXXGQKBgHJMGXTrFyo+UY+1LxEIzoHQyJeMdIUImHt+kFPnjTbVkGfHecNL\nLwl5J8pXG60KJKSbVKkBrcyVgMzzfx+ekCNOSzmi5T6q/qlvsso8AqtdRIH8a+iG\nz2h1Y7/errZ1S78Id7nXcJCiXyO6+YrC6MybuzS2P2fkPpRCzJ0VtjEvAoGAGXsZ\nu78szTuNOJXLwxLfin6siGQCQAG3WY4tkf+H8LZVl9h/Ip18X4x/dq3N2q++aQAJ\n7ilV77/fArPvYvO7X6MBe1RqUgQSWv9AlBvM1/iBkWcgxiBY2csQG6U0QLr/T+B4\nHAcQPDbC9lKWBSObWTgwqbDbq15xpQyCzaW7CTkCgYATpDTqOXPhwYZaxppUQ5NP\n6cuciaf4HeJq4xoV2kb9ZquoTeyCxHpST68+l7riD5WTjL6ulzz61yeQt9R2yve5\nnxKVc8G2fH0ZgcaBeLa202kCMmtmM5YvrvY1esOxSfKNWzwrw1gYdMkDthBwTdFZ\nx7wqBisicPGVja266T9ewg==\n-----END PRIVATE KEY-----\n",
  "client_email": "sohrawardy@curious-domain-385602.iam.gserviceaccount.com",
  "client_id": "105999517639164576623",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sohrawardy%40curious-domain-385602.iam.gserviceaccount.com"
}
'''

service_account = 'sohrawardy@curious-domain-385602.iam.gserviceaccount.com'


# Preparing values
json_object = json.loads(json_data, strict=False)
json_object = json.dumps(json_object)

# Authorising the app
credentials = ee.ServiceAccountCredentials(service_account, key_data=json_object)
ee.Initialize(credentials)

# Set page title
st.set_page_config(page_title='Streamlit Map Drawing Example')



Map = folium.Map()

Map = folium.Map()
folium.plugins.MeasureControl().add_to(Map)


# Add the draw control to the map
draw_control = Draw(export=True)
draw_control.add_to(Map)
st.write(draw_control)

folium_static(Map)

# Create a Streamlit button to capture the drawn features
if st.button("Capture Drawn Features"):
    drawn_json = draw_control.draw.get_data()
    features = drawn_json["features"]

    # Extract the coordinates from the features
    coordinates = features[0]["geometry"]["coordinates"][0]
    roi = Polygon(coordinates)

    # Print the coordinates of the drawn region
    st.write("Coordinates of the drawn region:", roi)




