'''
Created on 01-Feb-2021

@author: Abhishek Prajapati
'''
from abc import ABCMeta, abstractmethod 


class RazorPy(metaclass=ABCMeta):
    
    @abstractmethod
    def execute(self):
        pass