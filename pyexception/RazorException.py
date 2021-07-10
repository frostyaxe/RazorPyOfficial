'''
Created on 30-Jan-2021

@author: Abhishek Prajapati
'''
import support.razor_logger as logger


class RazorException(Exception):


    EXECERROR = "You cannot import this file as a module. Please run this file as a program."
    URLNF = "Application base URL not found."
    APIPATHNF = "API path not found"
    MISSINGAUTHSCHEME = "Authentication scheme is missing."
    BEARERAUTHTOKENNF = "Bearer authentication token is missing."
    BASICUSERNAMENF = "Username is missing for the basic authentication."
    BASICUSERPASSNF = "Password is missing for the basic authentication."
    UNSUPPORTEDAUTHSCHEME = "Unsupported Authentication Scheme found."
    SOMETHINGWENTWRONG = "Something went wrong!"    
    INVALIDTASKKEY= "Invalid key provided to the task. "
    INVALIDDATA = "Invalid data provided. "
    DATAMISSING = "Data is missing."
    
    def __init__(self, message):
        self.message = message
        logger.logger.error(message)
        super(RazorException, self).__init__(message)
        
    def __str__(self):
        return self.message
        