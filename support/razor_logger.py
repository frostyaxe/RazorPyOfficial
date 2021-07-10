'''
    
    Description: This python file handles logging the messages at the framework level
    @author: Abhishek Prajapati
    @version: V1.0
    @since: 30-01-2021

'''

import logging.config
from os import makedirs, sep
from os.path import join as join_path, exists as path_exists
import sys
from managers.vars_manager import AppsVars


log_dir = join_path(AppsVars.PROJECT_ROOT_DIR, 'logs')
if not path_exists(log_dir):
    makedirs(log_dir)
log_path = join_path(log_dir, 'razor_framework.log').replace(sep, '/')
if not path_exists(log_path):
    open(log_path, 'a').close()
logging.config.fileConfig(join_path(AppsVars.PROJECT_ROOT_DIR,'configuration/logging.ini'), disable_existing_loggers=False, defaults={ 'filename': log_path})
logger = logging.getLogger(__name__)
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)
logger.addHandler(stderr_handler)
logger.info("Logging is successfully started!")