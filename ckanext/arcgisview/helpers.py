# ckanext/iframe/helpers.py
import ckan.plugins.toolkit as tk
from ckanext.arcgisview.utils import get_arcgis_token
import time
import logging
log = logging.getLogger(__name__)


arcgis_token_cache ={
    'token': None,
    'expires': 0
}
def get_arcgis_token_helper():
    username = tk.config.get('ckanext.arcgis.username')
    password = tk.config.get('ckanext.arcgis.password')
    referer = tk.config.get('ckanext.arcgis.referer')
    arc_gis_url = tk.config.get('ckanext.arcgis.url')

    if not all([username, password, referer, arc_gis_url]):
        log.error("One or more configuration values are missing")
        raise ValueError("One or more configuration values are missing")
    current_time = time.time()
    current_time = int(current_time)*1000
    if arcgis_token_cache['token'] and current_time < arcgis_token_cache['expires']:
        log.info('Using cached ArcGIS token')
        return arcgis_token_cache['token']
    
    log.info('Cached ArcGIS token expired or not found, fetching new token')
    try:
        token, expires = get_arcgis_token(username, password, referer, arc_gis_url)
        arcgis_token_cache['token'] = token
        arcgis_token_cache['expires'] = expires
        log.info('New ArcGIS token obtained and cached')
        return token
    except Exception as e:
        log.error('Error obtaining ArcGIS token: {}'.format(e))
        return None

def register_helpers():
    return {
        'get_arcgis_token': get_arcgis_token_helper
    }
