# ckanext/iframe/utils.py
import requests



def get_arcgis_token(username, password, referer, arc_gis_url):
   
    payload = {
        'username': username,
        'password': password,
        'referer': referer,
        'f': 'json'
    }
    response = requests.post(arc_gis_url, data=payload)
    response_json = response.json()
    if 'token' in response_json:
        return response_json['token'] , response_json['expires']
    else:
        raise Exception('Error obtaining token: {}'.format(response_json))
