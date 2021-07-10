'''
Created on 01-Feb-2021

@author: Abhishek Prajapati
'''
from razorpy_abstract.RazorPy import RazorPy
import cowsay
from support.razor_logger import logger
import sys
import warnings

class Cowsay(RazorPy):
    '''
        Description: This class displays the message based on the cowsay character specified by the user in task.
        @author: Abhishek Prajapati
        @since: 01-Feb-2021
        @version: V1.0
    '''

    def __init__(self):
        '''
            Initialization of the variables with the default values.
        '''
        self.__cowsay_character = "tux"
        self.__message = None
    
    
    
    '''
        
        Description: Properties required to handle the execution based on the input specified by the user.
    
    '''
    
    @property
    def character(self):
        return self.__cowsay_character
    
    
    @character.setter
    def character(self, cowsay_character):
        self.__cowsay_character = cowsay_character
            
    @property
    def message(self):
        return self.__message
    
    @message.setter
    def message(self, cowsay_message):
        self.__message = cowsay_message
     
     
    ''' End of all the properties ''' 
     
    
    
    def execute(self):
        
        '''
        
            Description: Handles the execution flow of this service.
            @author: Abhishek Prajapati
            @since: 01-Feb-2021
            @version: V1.0
        
        '''
        
        if hasattr(cowsay, self.character):
            if not self.message:
                err_msg = "Message is not provided in the task. Please specify your custom message using `message` parameter in this task!"
                logger.error(err_msg)
                warnings.warn(err_msg)  
            getattr(cowsay, self.character)(self.message)
            
        else:
            err_msg = "{0} character not found in the cowsay module. Using default character Tux".format(self.character)
            logger.warn(err_msg)
            sys.stderr.write(err_msg)
            
        
        return self.message
        