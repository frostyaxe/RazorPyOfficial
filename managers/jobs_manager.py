'''
Created on 01-Feb-2021

@author: Abhishek Prajapati
'''

from json import loads, dumps
import sys
from time import time, sleep
from jinja2 import Template
from os import path
from managers.service_object_manager import ObjectManager
from managers.vars_manager import AppsVars
from pyexception.RazorException import RazorException
from razorpy_abstract.RazorPy import RazorPy
from support.razor_display import RazorPyDisplay
from support.razor_logger import logger
from utils.yaml_utils import YamlUtils
from managers import exec_details_manager

class JobManager(object):
    
    def __init__(self, jobs_json_obj):
        self.__jobs_json_obj = jobs_json_obj
        self.__services_object_manager = None
        self.__user_defined_vars = AppsVars()
        self.__default_capture = "console"
        self.__destination = None
   
        
        
    def execute(self):
        try:
            
            jobs = self.__jobs_json_obj['jobs']
            task_counter = 0
            for job in jobs:
                task_counter+=1
                self.__services_object_manager = ObjectManager()
                get_services_dict = self.__services_object_manager.get()
                job_modules = job.keys() 
                for job_module in job_modules:
                    if(job_module in get_services_dict):
                        service_obj = get_services_dict[job_module]
                        if not isinstance(service_obj, RazorPy):
                                    err_msg="{0} job module is not a RazorPy service!".format(job_module)
                                    logger.critical(err_msg)
                                    exit(err_msg)
                        tasks = job[job_module]
                        try:
                            exec_data = {}
                            if 'name' in tasks.keys():
                                task_title = tasks['name']
                               
                            else:
                                task_title = "RazorPy Task: {0}".format(task_counter)
                                tasks['name'] = task_title
                            RazorPyDisplay.display_task("Task execution started : : {0}".format(task_title))
                            
                            exec_data["task"] = task_title
                            
                            if "disabled" in tasks.keys():
                                if type(tasks["disabled"]) != bool:
                                    raise TypeError("Disabled key in the task only takes boolean value True and False. Expected bool found {0}".format(type(tasks["disabled"]) )) 
                                
                                else:
                                    if tasks["disabled"] == True:
                                        msg="Skipping current task: {0}".format(tasks["name"])
                                        exec_data["status"] = "Skipped"
                                        logger.warn(msg)
                                        print(msg)
                                        exec_data["output"] = msg
                                        exec_data["time"] = 0
                                        exec_details_manager.execution_details.append(exec_data)   
                                        del exec_data
                                        continue
                        finally:
                            
                            del tasks['name']
                        
                        if 'vars' in tasks.keys():
                            self.__load_vars(tasks)
                        
                        if 'capture' in tasks.keys():
                            if 'type' in tasks['capture']:
                                self.__default_capture = tasks['capture']['type']
                                if self.__default_capture == 'var':
                                    if 'name' in tasks['capture']:
                                        self.__destination = tasks['capture']['name']
                                    else:
                                        raise RazorException(RazorException.INVALIDDATA + " Name must be specified if capture type is var or file")    
                                        exit(1)
                                elif self.__default_capture == 'console':
                                    pass
                                else:
                                    raise  RazorException(RazorException.INVALIDDATA+ " Invalid capture type provided. Valid values are console, var and file.")        
                            else:
                                msg = "Type is not present in the capture! Using console to capture output."
                                logger.warn(msg)
                                print("[ Warning ] " + msg)
                            
                        if hasattr(service_obj, "razor_vars"):
                            setattr(service_obj, 'razor_vars', self.__user_defined_vars)
                        
                        for task,value in tasks.items():
                            ## Looking for alternativ to verify whether the given value has the Jinja2 template string or not 
                            
                            val_type = None
                            if type(value) != str:
                                val_type = type(value)
                                value = dumps(value)
                            
                            try:
                                value = Template(value)
                                value = value.render(self.__user_defined_vars.user_vars)
                            except TypeError as type_err_obj:
                                if str(type_err_obj).lower().find("can't compile non template nodes") == -1:
                                    raise TypeError(str(type_err_obj))
                                
                            if val_type:
                                value = loads(value)
                          
                            if( hasattr(service_obj, task)):
                                setattr(service_obj,task,  value)
                            else:
                                logger.warning("[ {0} ] Service object does not have attribute {1}.".format(job_module, task))
                        try:    
                            start_time = time()
                            output = service_obj.execute()
                            if self.__default_capture == "console":   
                                print("[ Output ] {0}".format(output))
                            elif self.__default_capture == "var":
                                self.__user_defined_vars.user_vars.update({self.__destination : output})
                                print('[ INFO ] Returned value is stored in variable -> {0}'.format(self.__destination))
                            
                            ## Pending for file storage!
                            
                            else:
                                pass 
                            exec_data["status"] = "Success"
                        except Exception as e:    
                           
                            exec_data["status"] = "Failure"
                            output = e.__class__.__name__ + " :: " + str(e)
                            logger.error(output)
                        finally:
                            exec_in_sec = time() - start_time
                            exec_data["time"] = exec_in_sec
                            exec_data["output"] = output
                            
                            del output
                            print('') 
                            self.__default_capture = "console"
                            self.__destination = None
                    else:
                        err_msg = "Unable to find service : : {0}".format(job_module)
                        logger.critical(err_msg)
                        sys.exit(err_msg)
                        
                    exec_details_manager.execution_details.append(exec_data)   
                    del exec_data
                        
        except Exception as err_obj:
            raise RazorException(RazorException.SOMETHINGWENTWRONG + " [ Error ] " + str(err_obj)) 
        finally:
            del self.__user_defined_vars.user_vars 
            exec_details_manager.razor_status = "Completed"
            self.__generate_report__()        
            print("Application will exit after 10 seconds...")
            sleep(30)        
    
    
    
    def __generate_report__(self):
        from jinja2 import Environment, FileSystemLoader
        file_loader = FileSystemLoader(path.join(AppsVars.PROJECT_ROOT_DIR,'templates'))
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        
        template = env.get_template('reporter.tpl')
        
        output = template.render(execution_details=exec_details_manager.execution_details)
        
        from datetime import datetime
        report_name = "razorpy-report-{0}.html".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        
        report_file_path = path.join(AppsVars.CURRENT_DIR,report_name)
        with open(report_file_path, "w") as report_file_obj:
            report_file_obj.write(output)
            
        import webbrowser
        webbrowser.open('file:///{0}'.format(report_file_path))
                    
    def __load_vars(self, tasks):
        
        if 'include' in tasks['vars']:
            yaml_file_path = ""
            yaml_loaded_content = YamlUtils().load(yaml_file_path)
            self.__user_defined_vars.user_vars.update(loads(yaml_loaded_content))
            del tasks['vars']['include']
            
        self.__user_defined_vars.user_vars.update(tasks['vars'])
        del tasks['vars']
        