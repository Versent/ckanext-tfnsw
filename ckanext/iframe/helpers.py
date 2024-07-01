# ckanext/iframe/helpers.py
import ckan.plugins.toolkit as tk
from ckanext.iframe.utils import get_arcgis_token
import time
import logging
log = logging.getLogger(__name__)


arcgis_token_cache ={
    'token': None,
    'expires': 0
}
def get_arcgis_token_helper():
    username = tk.config.get('ckan.arcgis.username')
    password = tk.config.get('ckan.arcgis.password')
    referer = tk.config.get('ckan.arcgis.referer')
    arc_gis_url = tk.config.get('ckan.arcgis.url')

    current_time = time.time()
    if arcgis_token_cache['token'] and current_time < arcgis_token_cache['expires']:
        log.info('Using cached token')
        return arcgis_token_cache['token']
    
    log.info('Cached token expired or not found, fetching new token')
    try:
        token, expires = get_arcgis_token(username, password, referer, arc_gis_url)
        arcgis_token_cache['token'] = token
        arcgis_token_cache['expires'] = expires
        log.info('New token obtained and cached')
        return token
    except Exception as e:
        log.error('Error obtaining token: {}'.format(e))
        return None

def register_helpers():
    return {
        'get_arcgis_token': get_arcgis_token_helper
    }
