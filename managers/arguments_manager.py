'''
Created on 30-Jan-2021

@author: Abhishek Prajapati
'''

from support.razor_logger import logger


class ArgumentsManager(object):
    '''
    classdocs
    '''
   

    def __init__(self):
        '''
        Constructor
        '''
        from argparse import ArgumentParser
        self.__args_parser = ArgumentParser()
        self.__parsed_args = None
    
    
    
    def load_arguments(self):
        logger.info("Loading all the required arguments...")
        self.__args_parser.add_argument('-f', '--file', type=str, help='Path of the razor YAML files containing the required actions to be performed.')
        
        logger.info("Arguments added successfully in the parser...")
        logger.info("Parsing command line arguments....")
        self.__parsed_args = self.__args_parser.parse_args() 
        logger.info("Arguments parsed successfully!")
        return self
    
    def get_arg_value(self, arg_key):
        if arg_key in self.__parsed_args:
            return getattr(self.__parsed_args,arg_key)
        else:
            err_msg = 'Unable to retrieve value from the parsed argument using the following key: {1}'.format(arg_key)
            logger.error(err_msg)
            raise KeyError(err_msg)
            
    