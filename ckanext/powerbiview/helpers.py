# ckanext/powerbi/helpers.py
import ckan.plugins.toolkit as tk
import time
import logging
import msal
import requests
import json
log = logging.getLogger(__name__)



def get_powerbi_config_helper(group_id,report_id, is_dashboard=False):
    try:
        
        # Get configurations from the ckan.ini file, is_dashboard is used to execute the code for dashboard
        client_id= tk.config.get('ckanext.powerbi.client_id')
        client_secret= tk.config.get('ckanext.powerbi.client_secret')
        tenant_id= tk.config.get('ckanext.powerbi.tenant_id')
        scope_base= "https://analysis.windows.net/powerbi/api/.default"
        authority_url= "https://login.microsoftonline.com/"+tenant_id


        
        #check if any of the config is missing, if missing return an error message
        if not all([client_id, client_secret, authority_url, tenant_id, scope_base, group_id, report_id]):
            log.error("One or more configuration values are missing in Power BI configuration")
            return None
        

        #Get the access token 
        access_token= get_access_token(client_id,client_secret,authority_url)
        # If we are working with a report
        if access_token and not is_dashboard:
            log.info('Generating Embed Config for Power Bi Report')
            report_url = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}'
            headers = { 
                'Content-Type': 'application/json', 
                'Authorization': f'Bearer {access_token}'
                }
            
            # Fetch report information
            pbi_report_info_response = requests.get(report_url, headers=headers)
            if pbi_report_info_response.status_code != 200:
                log.error(f"Failed to fetch report info: {pbi_report_info_response.status_code} - {pbi_report_info_response.text}")
                return None, None
            pbi_report_info_response = json.loads(pbi_report_info_response.text)
            #Create request body for the embeded token api call, this is only required 
            # datasets = [{"id": dataset_id} for dataset_id in [pbi_dashboard_info_response['datasetId']]]
            # reports = [{"id": report_id}]
            # workspaces = [{"id": group_id}] if group_id else []
            # embed_token_api = 'https://api.powerbi.com/v1.0/myorg/GenerateToken'
            # data=json.dumps({'datasets': datasets, 'reports': reports, 'workspaces': workspaces})

            data=json.dumps({"accessLevel": "View"})
            pbi_report_embed_token_response =requests.post(report_url+"/GenerateToken", data=data, headers=headers)
            if pbi_report_embed_token_response.status_code != 200:
                log.error(f"Failed to generate embed token: {pbi_report_embed_token_response.status_code} - {pbi_report_embed_token_response.text}")
                return None, None
            pbi_report_embed_token_response = pbi_report_embed_token_response.json()
            if 'token' not in pbi_report_embed_token_response:
                log.error("Embed token not found in response for Power BI report /GenerateToken api call")
                return None, None
            log.info("Successfully fetched embed URL and token")
            return pbi_report_info_response['embedUrl'], pbi_report_embed_token_response['token']

        elif access_token and is_dashboard:
            log.info('Generating Embed Config for Power Bi Dashboard')
            dashboard_url = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/dashboards/{report_id}'
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                }
            pbi_dashboard_info_response = requests.get(dashboard_url, headers=headers)
            if pbi_dashboard_info_response.status_code != 200:
                log.error(f"Failed to fetch dashboard info: {pbi_dashboard_info_response.status_code} - {pbi_dashboard_info_response.text}")
                return None, None
            pbi_dashboard_info_response = json.loads(pbi_dashboard_info_response.text)
            data=json.dumps({"accessLevel": "View"})
            pbi_dashboard_embed_token_response =requests.post(dashboard_url+"/GenerateToken", data=data, headers=headers)
            if pbi_dashboard_embed_token_response.status_code != 200:
                log.error(f"Failed to generate embed token: {pbi_dashboard_embed_token_response.status_code} - {pbi_dashboard_embed_token_response.text}")
                return None, None
            pbi_dashboard_embed_token_response = json.loads(pbi_dashboard_embed_token_response.text)
            if 'token' not in pbi_dashboard_embed_token_response:
                log.error("Embed token not found in response for Power BI dashboard /GenerateToken api call")
                return None, None
            log.info("Successfully fetched embed URL and token")
            return pbi_dashboard_info_response['embedUrl'],pbi_dashboard_embed_token_response['token']
        else:
            log.error("Failed to get access token")
            return None, None
        
    except requests.RequestException as e:
        log.error(f"Request failed: {e}")
        return None, None
    except json.JSONDecodeError as e:
        log.error(f"Failed to parse JSON response: {e}")
        return None, None

def register_helpers():
    return {
        'get_powerbi_config': get_powerbi_config_helper
    }

def get_access_token(client_id,client_secret,authority_url):
    try:
        client = msal.ConfidentialClientApplication(client_id,  client_credential=client_secret, authority=authority_url)
        result = client.acquire_token_for_client(scopes=["https://analysis.windows.net/powerbi/api/.default"])
        #log.error(result)
        if "access_token" in result:
            return result['access_token']
        return None
    except Exception as ex:
        log.error('Error retrieving PowerBI token: {}'.format(ex))
        return None


