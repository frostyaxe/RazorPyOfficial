'''
Created on 30-Jan-2021

@author: Abhishek Prajapati
'''

import os


class AppsVars(object):


    __CURRENT_DIR = os.getcwd()
    __PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath("application.py"))
    
    def __init__(self):
        self.__user_vars = {}
    
    @classmethod
    @property 
    def PROJECT_ROOT_DIR(cls):
        return AppsVars.__PROJECT_ROOT_DIR
    
    @classmethod
    @property
    def CURRENT_DIR(cls):
        return AppsVars.__CURRENT_DIR
    
    @property
    def user_vars(self):
        return self.__user_vars
    
    @user_vars.setter
    def user_vars(self, user_vars):
        self.__user_vars.update(user_vars)

    @user_vars.deleter
    def user_vars(self):
        del self.__user_vars 
    

