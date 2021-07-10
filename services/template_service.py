'''
Created on 05-Feb-2021

@author: Abhishek Prajapati
'''
from os import path

from jinja2 import Environment, FileSystemLoader

from managers.vars_manager import AppsVars
from pyexception.RazorException import RazorException
from razorpy_abstract.RazorPy import RazorPy
import ntpath


class Template(RazorPy):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__template_string = None
        self.__template_file = None
        self.__razor_vars = None
     
     
    @property   
    def string(self):
        return self.__template_string
    
    @string.setter
    def string(self, template_string):
        self.__template_string = template_string
        
    @string.deleter
    def string(self):
        del self.__template_string
        
    @property   
    def file(self):
        return self.__template_file
    
    @file.setter
    def file(self, template_file):
        self.__template_file = template_file
        
    @file.deleter
    def file(self):
        del self.__template_file
        
    @property   
    def razor_vars(self):
        return self.__razor_vars
    
    @razor_vars.setter
    def razor_vars(self, razor_vars):
        self.__razor_vars = razor_vars
        
    @razor_vars.deleter
    def razor_vars(self):
        del self.__razor_vars
        
    def execute(self):
        if self.string:
            return self.string
        elif self.file:
            file_loader = FileSystemLoader('templates')
            env = Environment(loader=file_loader)
            env.trim_blocks = True
            env.lstrip_blocks = True
            env.rstrip_blocks = True
            
            if not path.exists(self.file):
                file_temp = path.join(AppsVars.CURRENT_DIR,self.file)
                if path.exists(file_temp):
                    self.file = file_temp
                    
                elif path.exists(path.join(AppsVars.PROJECT_ROOT_DIR,self.file)): self.file = path.join(AppsVars.PROJECT_ROOT_DIR,self.file)
                else: 
                    raise FileNotFoundError("Unable to find template file at given location: {0}".format(self.file) )
                    exit(1)
            temp_dir = path.dirname(path.abspath(self.file))
            self.file = ntpath.basename(self.file)
            file_loader = FileSystemLoader(temp_dir)
            env = Environment(loader=file_loader)
            template = env.get_template(self.file)
            return template.render(self.razor_vars.user_vars)
        else:
            raise RazorException(RazorException.INVALIDTASKKEY + "Please provide either string or file in this task.")
                
    