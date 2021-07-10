'''
Created on 15-Jun-2021

@author: Abhishek Prajapati
'''
from  services.url_service import URL
from razorpy_abstract.RazorPy import RazorPy
from support.razor_logger import logger
from utils.assertutils import AssertUtils
from json import loads, dumps
import lxml.etree as ET
from jsonpath_ng import parse
from urllib.parse import urlencode

class APITEST(RazorPy):
    
    def __init__(self):
        self.__url_service_obj = URL()
        self.__validators = None
        self.__response_type = ""
        self.__assert_utils_obj = AssertUtils()
        self.__query_params = {}
        self.__output = ""
        
    @property
    def base_url(self):
        return self.__url_service_obj.base_url
    
    @base_url.setter
    def base_url(self, app_base_url):
        self.__url_service_obj.base_url = app_base_url
        
    @property
    def api_path(self):
        return self.__url_service_obj.api_path
    
    @api_path.setter 
    def api_path(self, app_api_path):
        self.__url_service_obj.api_path = app_api_path
    
    
    @property
    def query_param(self):
        return self.__query_params
    
    @query_param.setter 
    def query_param(self, query_param):
        self.__query_params = query_param
        
    @property
    def request(self):
        return self.__url_service_obj.request
    
    @request.setter
    def request(self, rest_request_method):
        self.__url_service_obj.request = rest_request_method
        
    @property
    def authentication(self):
        return self.__url_service_obj.authentication
    
    @authentication.setter
    def authentication(self,  authentication_details):
        self.__url_service_obj.authentication = authentication_details
        
    @property
    def headers(self):
        return self.__url_service_obj.headers
    
    @headers.setter
    def headers(self, request_headers):
        self.__url_service_obj.headers = request_headers
        
    @property
    def response_type(self):
        return self.__response_type
    
    @response_type.setter
    def response_type(self, reponse_type):
        self.__response_type = reponse_type
    
    @property
    def validators(self):
        return self.__validators
        
    @validators.setter
    def validators(self, validators):
        self.__validators = validators
        
    def __pr3par3_qu3ry_param3t3rs__(self):
        if self.query_param:
            self.__url_service_obj.api_path += "?"+urlencode(self.query_param)
     
    def __expected_status__(self, actual, expected): 
        try:
            assert actual in expected
            info_msg="Actual status code: {0} is present in the expected status code list: {1}".format(actual,expected)
            print(info_msg)
            self.__output += info_msg + " || "
            logger.info(info_msg)
        except AssertionError as e:
            err_msg = "Actual status code: {0} is not present in the expected status code list: {1}".format(actual,expected)
            logger.error(err_msg)
            self.__output += err_msg + " || "
            raise e
            
    def __assertion__(self, operator, actual, expected):  
        AssertUtils().assert_handler(operator, actual, expected)
    
    
    def __verify_content__(self):
        
        if "expected_status" in self.validators: 
            if type(self.validators["expected_status"]) != list:
                raise TypeError("Expected status must be provided in the list format.")
        if type(self.query_param) != dict:
            raise TypeError("Type of query parameters must be dictionary found {0}".format(type(self.query_param)))
        if "compare" in self.validators:
            if type(self.validators["compare"]) != list:
                raise TypeError("Compare section must be provided in the list format.")
          
               
        expected_response_types = [ "xml", "json" ]
        if self.response_type not in expected_response_types:
            raise ValueError("Currently this framework supports only following response types: {0}. Please specify response type in the yaml file using key as response_type.".format(expected_response_types))
                
    def execute(self):
        self.__verify_content__()
        self.__pr3par3_qu3ry_param3t3rs__()
        api_response = self.__url_service_obj.execute()
        if api_response.status != 200:
            print("Rest API has returned an error message: {0}".format(api_response.reason))
            print(api_response.msg)
            logger.info("Retrieved headers: {0}".format(api_response.headers))
        logger.info(api_response.data)
        self.__expected_status__(api_response.status, self.validators["expected_status"])
        if "compare" in self.validators:
            for compare_data in self.validators["compare"]:
                if "json_path" not in compare_data and "xml_path" not in compare_data:
                    raise ValueError("Please specify either JSON path or XML path using json_path or xml_path respectively.")
                    
                if "expected" not in compare_data:
                    raise ValueError("Please specify the expect value in the compare section using expected keyword.")
                output = None
                response_data = api_response.data
                if 'validate' in compare_data:
                    if "header" == compare_data["validate"].lower():
                        response_data = dumps(dict(api_response.headers))
                
                
                if self.response_type == 'xml':
                    xml_response = ET.ElementTree(ET.fromstring(response_data.decode('utf-8')))
                    #output = fcp.xml_content_processor(api_response, "xml_path", compare_data, {})
                    
                    
                elif self.response_type == 'json':
                    json_api_response = loads(response_data)
                    #output = fcp.json_content_processor(api_response, ["json_path"], compare_data, {})  
                    jsonpath_expression = parse(compare_data["json_path"])
                    output = [ match.value for match in jsonpath_expression.find(json_api_response) ]
                   
                comparator = None
                if "comparator" in compare_data:
                    comparator =  compare_data["comparator"]
                    
                for value in output:
                    if type(value) == str:
                        if value.isdigit():
                            value = int(value)
                    
                    print("[ API Response ] {0}".format(api_response.data))        
                    
        
        self.__output += self.__assert_utils_obj.assert_handler(comparator, value, compare_data['expected'])
        return self.__output
        
                
        
                    
                
        