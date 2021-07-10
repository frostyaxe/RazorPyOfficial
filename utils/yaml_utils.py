'''
Created on 30-Jan-2021

@author: Abhishek Prajapati
'''

#All os imports
from errno import ENOENT
from os import strerror
from os.path import exists as file_path_exists, join as join_path

from yaml import safe_load, YAMLError

from managers.vars_manager import AppsVars
from support.razor_logger import logger


class YamlUtils(object):
    '''
        
        Description: This utility file handles the required operations to be performed on the specified YAML file.
        @author: Abhishek Prajapati
        @since:  30-01-2021
        @version: V1.0
    
    '''
    
    
    def __init__(self):
        pass
    
    
    
    def load(self, yaml_file_path):
        '''
            
            Description: This method loads the content present in the YAML file with the help of stream.
            @author: Abhishek Prajapati
            @since: 30-01-2021
            @version: V1.0
            @return: loaded data of specified YAML file in the form of JSON.
            @param yaml_file_path: Path of the desired YAML file. 
            @raise YAMLError: It throws error when pyyaml module is unable to the content of specified YAML file properly. 
        
        '''
        
        if not file_path_exists(yaml_file_path):
            logger.info("YAML file does not exist at the given location: {0}".format(yaml_file_path))
            temp_path = join_path(AppsVars.CURRENT_DIR,yaml_file_path)
            logger.info("Searching file at the current location using following path: {0}".format(temp_path))
            if file_path_exists(temp_path):
                logger.info("Specified YAML file is present at the current location.")
                yaml_file_path = temp_path
            else:
                raise FileNotFoundError(ENOENT,strerror(ENOENT), yaml_file_path)
        
        with open(yaml_file_path, 'r') as yaml_file_stream:
            try:
                return safe_load(yaml_file_stream)
            except YAMLError as load_exception:
                logger.error(str(load_exception)) 
                raise YAMLError("Unable to load specified YAML file. File path: {0}".format(yaml_file_path))
            finally:
                yaml_file_stream.close()
            
                
    