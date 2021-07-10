'''
Created on 30-Apr-2021

@author: Abhishek Prajapati
'''
from razorpy_abstract.RazorPy import RazorPy

class Python(RazorPy):
    
    def __init__(self):
        self.__type = 'exec'
        self.__code_string = "print('Hello from RazorPy Python service!')"
        self.__razor_vars = {}
    
    @property    
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, service_type):
        self.__type = service_type
        
    @property
    def string(self):
        return self.__code_string
    
    @string.setter
    def string(self, code_string):
        self.__code_string = code_string
        
    @property
    def razor_vars(self):
        return self.__razor_vars
    
    @razor_vars.setter
    def razor_vars(self, razor_vars):
        self.__razor_vars = razor_vars
            
    def execute(self):
        
        if self.type == 'eval':
            return eval(self.string, self.razor_vars.user_vars)
        else:
            return exec(self.string, self.razor_vars.user_vars)
        