'''
Created on 28-Feb-2021

@author: Abhishek Prajapati
'''
import json
from os import walk, path
import re
from jinja2 import Template
import lxml.etree as etree
from managers.vars_manager import AppsVars
from pyexception.RazorException import RazorException
from razorpy_abstract.RazorPy import RazorPy
import utils.file_content_processor as fcp

class Gating(RazorPy):
    
    def __init__(self):
        self.__process_type = None
        self.__report_dir = AppsVars.CURRENT_DIR
        self.__filter = None
        self.__threshold = 0
        self.__dictionary = {}
        self.__process_pattern = None
        self.__result_dictionary = {}
        
        
    @property
    def process_type(self):
        return self.__process_type
    
    @process_type.setter
    def process_type(self, process_type):
        self.__process_type = process_type
        
    @property
    def report_dir(self):
        return self.__report_dir
    
    @report_dir.setter
    def report_dir(self, report_dir):
        self.__report_dir = report_dir
        
    @property
    def filter(self):
        return self.__filter
    
    @filter.setter
    def filter(self, filterval):
        self.__filter = filterval
        
        
    @property
    def threshold(self):
        return self.__threshold
    
    @threshold.setter
    def threshold(self, threshold):
        self.__threshold = threshold
        
    @property
    def dictionary(self):
        return self.__dictionary
    
    @dictionary.setter 
    def dictionary(self, dictionary):
        self.__dictionary = dictionary
    
    @property
    def process_pattern(self):
        return self.__process_pattern
    
    @process_pattern.setter
    def process_pattern(self, process_pattern):
        self.__process_pattern = process_pattern
        
    
    def retrieve_vars(self):
        
        rgx = re.compile('{{(?P<name>[^{}]+)}}')
        variable_names = {match.group('name') for match in rgx.finditer(self.process_pattern)}
        return variable_names
        
    def xml_processor(self, file, input_vars):
        with open(file, 'rb') as xml_file_obj:
            root = etree.XML(xml_file_obj.read())
            self.__result_dictionary.update(fcp.xml_content_processor(root, input_vars, self.dictionary, self.__result_dictionary))
    
    def json_processor(self, file, input_vars):
        
        with open(file,'rb') as json_file_obj:
            self.__result_dictionary.update(fcp.json_content_processor(json.load(json_file_obj), input_vars, self.dictionary, self.__result_dictionary))
                        
    
    def execute(self):
        self.__result_dictionary = {}
        if self.__filter == None:
            raise RazorException(RazorException.DATAMISSING + "Value for the file filter is missing in the yaml file. Please provide the required data using 'filter' key in yaml file.")
            exit('Error')
        regex = re.compile(self.filter)
        listOfFiles = list()
        for (dirpath, dirnames, filenames) in walk(self.report_dir):
            listOfFiles += [path.join(dirpath, file) for file in filenames  if regex.match(file) ]
        print(listOfFiles)        
        
        input_vars = self.retrieve_vars()
        
    
        for file in listOfFiles:
            if self.process_type == 'xml':
                self.xml_processor(file, input_vars)
            if self.process_type == "json":
                self.json_processor(file, input_vars)
                
                
        
        process_template = Template(self.process_pattern)
        evaluated_result = eval(process_template.render(self.__result_dictionary))
            
        if float(evaluated_result) > float(self.threshold):
            exit("Evaluated result[ {0} ] is greater than the threshold[ {1} ]".format(evaluated_result,self.threshold))
        else:
            print("Evaluated result[ {0} ] is less than the specified threshold[ {1} ]".format(evaluated_result,self.threshold))
