'''
Created on 30-Jan-2021

@author: Abhishek Prajapati
'''
from pyexception.RazorException import RazorException
from managers.jobs_manager import JobManager
from support.razor_display import RazorPyDisplay
import sys
from configuration import appconf

class Application(object):
    '''
        Description: This class is the entry point for all the execution that reads the data 
                    from the yaml file and based on that it performs the required task.
        
        @author: Abhishek Prajapati
        @since: 20-01-2021
        @version: V1.0        
    '''


    def __init__(self):
        from managers.arguments_manager import ArgumentsManager
        self.__args_manager = ArgumentsManager()
        sys.tracebacklimit=appconf.traceback
    
    
    def execute(self):
        RazorPyDisplay.display_head()
        loaded_args = self.__args_manager.load_arguments()
        from utils.yaml_utils import YamlUtils
        yaml_file_path = loaded_args.get_arg_value('file')
        from support.razor_logger import logger
        logger.info("Loading Razor YAML file content...")
        yaml_loaded_content = YamlUtils().load(yaml_file_path)
        jobs_manager = JobManager(yaml_loaded_content)
        jobs_manager.execute()
        

if '__main__' == __name__:
    Application().execute()
else:
    raise RazorException(RazorException.EXECERROR)
    