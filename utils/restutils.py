'''
Created on 01-Feb-2021

@author: Abhishek Prajapati
'''

from json import loads
import lxml.etree as ET
from urllib3 import PoolManager, make_headers 


class RestUtils(object):
    '''
        
        Description: This class handles the rest request based on the input provided by the user.
        @author: Abhishek Prajapati
        @since: 01-Feb-2021
        @version: V1.0
        
    '''


    def __init__(self):
        '''
           Initializes the instance variables with default values.
        '''
        self.__application_base_url = None
        self.__application_api_path = None
        self.__authentication_scheme = None
        self.__authentication_username = None
        self.__authentication_key = None
        self.__request_method =  None
        self.__response_type = None
        self.__pool_manager_obj = PoolManager()
        self.__headers = {}
        self.__payload = ""
        
        
    def base_url(self, app_base_url):
        if not app_base_url.endswith('/'):
            app_base_url = app_base_url + "/"
        self.__application_base_url = app_base_url
        return self
        
        
    def api_path(self, app_api_path):
        if app_api_path.startswith('/'):
            app_api_path = app_api_path.replace('/', '', 1)
        self.__application_api_path = app_api_path
        return self
    
    
    def basic_authentication(self, username, password):
        self.__headers.update(make_headers(basic_auth='{0}:{1}'.format(username,password)))
        return self
    
    def bearer_authentication(self, auth_token):
        self.__headers.update( {"Authorization":"Bearer {0}".format(auth_token) })
        return self
    
    def add_headers(self, request_headers):
        self.__headers.update(request_headers)
        return self
    
    def get_method(self):
        self.__request_method = 'GET'
        return self
    
    def post_method(self, payload):
        self.__request_method = 'POST'
        if payload:
            self.__payload = payload
        return self
    
    def put_method(self, payload):
        self.__request_method = 'PUT'
        if payload:
            self.__payload = payload
        return self   
    
    def delete_method(self):
        self.__request_method = 'DELETE'
        return self
        
    def get_response(self, response_type):   
        if response_type:
            self.__response_type = response_type
        response = self.__pool_manager_obj.request(self.__request_method,self.__application_base_url+self.__application_api_path, body=self.__payload, headers=self.__headers)
        if response_type.lower() == 'text':
            return response.data.decode('utf-8')
        elif response_type.lower() == 'json':
            return loads(response.data)
        elif response_type.lower() == 'xml':
            return ET.ElementTree(ET.fromstring(response.data.decode('utf-8')))
        else:
            return response
        
        
        
        