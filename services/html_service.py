'''
Created on 14-Feb-2021

@author: Abhishek Prajapati
'''
from msilib.schema import Component
import os

from jinja2 import Template
from pyautogui import alert

from managers.vars_manager import AppsVars
from pyexception.RazorException import RazorException
from razorpy_abstract.RazorPy import RazorPy


resources_dir = os.path.join(AppsVars.PROJECT_ROOT_DIR,"resources")
components_dir = os.path.join(resources_dir, "html_components")
templates_dir = os.path.join(resources_dir, "templates")
attribs_mapper = lambda data: [ '{key}="{value}"'.format(key=key,value=value) for key,value in data.items() ]
 
class HTML(RazorPy):
    
    def __init__(self):
        self.__html_components = None
        self.__loaded_existing_component_names = []
        self.__out_file = os.path.join(AppsVars.CURRENT_DIR,"index.html")
    
    
    @property
    def file(self):
        return self.__out_file
    
    @file.setter
    def file(self, file_name):
        self.__out_file = file_name    
    
    @property
    def components(self):
        return self.__html_components
    
    @components.setter
    def components(self, html_components):
        self.__html_components = html_components
        
    @components.deleter
    def components(self):
        del self.__html_components
    
    
    def __verify_components_data(self):
        if not isinstance(self.components, list):
            raise RazorException(RazorException.INVALIDDATA + " Components data must be present as list in the yaml file.")
            exit(1)  
            
    def __get_loaded_existing_component_names(self):
    
        self.__loaded_existing_component_names = list(map(lambda component_name: component_name.replace('.comp',''), list(os.walk(components_dir))[0][2]))
    
    def __get_loaded_component_template(self, component_name):
        components_dir = os.path.join(resources_dir, "html_components")
        component_path = os.path.join(components_dir,component_name+".comp")
        with open(component_path, 'r+') as comp_file_obj:
            return comp_file_obj.read()
    
    
    
    def __render_component(self,template_string, **kwargs):
        template = Template(template_string)
        return template.render(kwargs)
    
    def __table_handler(self,  component_template,  component_data):
        
        table_headings = ''
        table_rows = ''
   
        component_attribs = '' 
        header_attribs = ''
        data_attribs = ''
        
        if 'headings' in component_data:
            if not type(component_data['headings']) == list:
                raise RazorException(RazorException.INVALIDDATA+"Headings must be provided in the list format in YAML file.")
                exit(1)
            table_headings = component_data['headings']
        else:
            raise RazorException(RazorException.INVALIDDATA+"Please provide table column headings in the YAML data.")
            exit(1)
            
        if 'rows' in component_data:
            if not type(component_data['rows']) == list:
                raise RazorException(RazorException.INVALIDDATA+"Table rows must be provided in the list format in YAML file.")
                exit(1)
            from csv import reader
            table_rows = [ row.split(',') for row in component_data['rows'] ]
        else:
            raise RazorException(RazorException.INVALIDDATA+"Please provide table rows data in the YAML data.")
            exit(1)

        if 'attribs' in component_data:
            
            attributes = component_data['attribs']
            if 'component' in attributes:
                component_attribs = " ".join(attribs_mapper(attributes['component']))
                
            if 'header' in attributes:
                header_attribs = " ".join(attribs_mapper(attributes['header']))
            
            if 'data' in attributes:
                data_attribs = " ".join(attribs_mapper(attributes['data']  ))
              
        return self.__render_component(component_template, **{"table_attribs": component_attribs,"thead_attribs":header_attribs,"table_headings": table_headings, "table_row_data":table_rows})       
    
    
    def __alert_handler(self,  component_template,  component_data):
        alert_attribs = {'class': "alert"}
        close = "false"
        title = ""
        message = ""
        
        if 'title' in component_data:
            title += component_data['title']
    
        if 'message' in component_data:
            message += component_data['message']   
            
        if 'enableClose' in component_data:
            close = component_data['enableClose'].lower()
        
        if 'attribs' in component_data:    
            for k, v in component_data['attribs'].items():
                if k in alert_attribs:
                    alert_attribs[k] += " {0}".format(v)
                
                else:
                    alert_attribs[k] = v
        alert_attribs = " ".join(attribs_mapper(alert_attribs))  
        return self.__render_component(component_template, **{"alert_attribs":alert_attribs,"close":close, "message":message, "title":title })
                 
    def execute(self):
        body_content = ''
        self.__verify_components_data()
        self.__get_loaded_existing_component_names()
        for component in self.components:
            for k,v in component.items():
                if not k in self.__loaded_existing_component_names:
                    raise RazorException(RazorException.INVALIDDATA+"Component: {0} is not present in the RazorPy HTML components list.".format(k))
                    exit(1)
                
                component_handler_name = "_HTML__{0}_handler".format(k)
                component_template_string = self.__get_loaded_component_template(k)
                if hasattr(self, component_handler_name):
                    body_content += getattr(self, component_handler_name)(component_template_string,v) + "\n"
                else:
                    raise RazorException(RazorException.INVALIDDATA + "Handler for specified component: {0} is not present in the HTML service. Please contact developer to add it!".format(k))
        
        base_template = os.path.join(templates_dir,"base.html")
        if os.path.exists(base_template):
            with open(base_template) as base_template_obj:
                with open(self.file, 'w+') as out_file:
                    out_file.write(self.__render_component(base_template_obj.read(), **{'body_content':body_content}))
                base_template_obj.close()
                out_file.close()
                return "HTML file successfully at the following location: {0}".format(self.file)
        else:
            raise RazorException(RazorException.SOMETHINGWENTWRONG + "Base template does not exist!")
        exit(1)