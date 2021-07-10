'''
Created on 01-Feb-2021

@author: Abhishek Prajapati
'''
from pyexception.RazorException import RazorException
from razorpy_abstract.RazorPy import RazorPy
from support.razor_logger import logger
from utils.restutils import RestUtils
from urllib.parse import urlencode

class URL(RazorPy):
    '''
        
        Description: This class handles the calls related to the rest api with the help of urllib3 module.
        @author: Abhishek Prajapati
        @since: 02-Feb-2021
        @version: V1.0
        
    '''


    def __init__(self):
        '''
            Initializes the instance variables with default values.
        '''
        self.__app_base_url = None
        self.__app_api_path = None
        self.__request_method = 'GET'
        self.__authentication = None
        self.__req_headers = None
        self.__response_type = 'obj'
        self.__request = None
        self.__query_params = {}
    
    
    @property
    def base_url(self):
        return self.__app_base_url
    
    @base_url.setter
    def base_url(self, app_base_url):
        self.__app_base_url = app_base_url
        
    @property
    def api_path(self):
        return self.__app_api_path
    
    @api_path.setter 
    def api_path(self, app_api_path):
        self.__app_api_path = app_api_path
    
    
    @property
    def query_param(self):
        return self.__query_params
    
    @query_param.setter 
    def query_param(self, query_param):
        self.__query_params = query_param
        
    @property
    def request(self):
        return self.__request
    
    @request.setter
    def request(self, rest_request_method):
        self.__request = rest_request_method
        
    @property
    def authentication(self):
        return self.__authentication
    
    @authentication.setter
    def authentication(self,  authentication_details):
        self.__authentication = authentication_details
        
    @property
    def headers(self):
        return self.__req_headers
    
    @headers.setter
    def headers(self, request_headers):
        self.__req_headers = request_headers
        
    @property
    def response_type(self):
        return self.__response_type
    
    @response_type.setter
    def response_type(self, resp_type):
        self.__response_type = resp_type
        
    def __pr3par3_qu3ry_param3t3rs__(self):
        if self.query_param:
            self.api_path += "?"+urlencode(self.query_param)
            
    def execute(self):
        if self.base_url:
            if self.api_path:
                self.__rest_obj = RestUtils().base_url(self.base_url).api_path(self.api_path)
                if type(self.query_param) != dict:
                    raise TypeError("Type of query parameters must be dictionary found {0}".format(type(self.query_param)))
                self.__pr3par3_qu3ry_param3t3rs__()
                if self.authentication:
                    if 'scheme' in self.authentication:
                        scheme = str(self.authentication['scheme']).lower()
                        if scheme == "bearer": 
                            if 'token' in self.authentication:
                                self.__rest_obj.bearer_authentication(str(self.authentication['token']))
                            else:
                                self.__raise_err_and_exit(RazorException.BEARERAUTHTOKENNF)
                        elif scheme == "basic":
                            if 'username' in self.authentication:
                                if 'password' in self.authentication:
                                    self.__rest_obj.basic_authentication(str(self.authentication['username']), str(self.authentication['password']))
                                else:
                                    self.__raise_err_and_exit(RazorException.BASICUSERPASSNF)
                            else:
                                self.__raise_err_and_exit(RazorException.BASICUSERNAMENF)
                        else:
                            self.__raise_err_and_exit(RazorException.UNSUPPORTEDAUTHSCHEME)
                    else:
                        self.__raise_err_and_exit(RazorException.MISSINGAUTHSCHEME)
                if self.headers:
                    request_headers = {}
                    for header in self.headers:
                        request_headers.update(header)
                    self.__rest_obj.add_headers(request_headers)
                
                if self.request != None and 'method' in self.request:
                    if self.request['method'].lower() == 'post' or self.request['method'].lower() == 'put' :
                        payload = ""
                        if 'payload' in self.request:
                            payload =str( self.request['payload'] )
                        if self.request['method'].lower() == 'post':
                            self.__rest_obj.post_method(payload)
                        elif self.request['method'].lower() == 'put':
                            self.__rest_obj.put_method(payload)
                        else:
                            self._raise_err_and_exit("Unable to find the request method provided by the user!")    
                    elif self.request['method'].lower() == 'delete':
                        self.__rest_obj.delete_method()
                    else:
                        self.__rest_obj.get_method()
                else:
                    self.__rest_obj.get_method()   
                
                if self.response_type:
                    self.__response_type = self.response_type
                    
                return self.__rest_obj.get_response(self.response_type)
                            
            else:
                self.__raise_err_and_exit(RazorException.APIPATHNF)
        else:
            self.__raise_err_and_exit(RazorException.URLNF)
            
            
    def __raise_err_and_exit(self, errmsg):
        logger.error(errmsg)
        raise RazorException(errmsg)
        exit(1)