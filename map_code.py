import base64
import folium

encoded_image = base64.b64encode(open("location_icon.png", "rb").read())
decoded_image = encoded_image.decode()


mapa = folium.Map(location=[7.148202,-73.135969], zoom_start=5)

feature_group = folium.FeatureGroup('markers')
icon_url = 'data:image/png;base64,' + f'{decoded_image}'
#print (icon_url)

def map_code(data, language):

	for feature in data:

		if language == "es":
			popup_text = feature["properties"]["Popup_es"]
		else:
			popup_text = feature["properties"]["Popup_en"]

		folium.Marker(location=list(feature['geometry']['coordinates']),
			icon = folium.features.CustomIcon(icon_url,icon_size=(40, 40)),
			popup=popup_text
			).add_to(feature_group)

	feature_group.add_to(mapa)
	mapa.save("Mapa_send.html")




