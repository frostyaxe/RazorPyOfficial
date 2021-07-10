'''
Created on 01-Feb-2021

@author: Abhishek Prajapati
'''
import importlib
import inspect
import pkgutil
import services
from support.razor_logger import logger

class ObjectManager:
  
    def __init__(self):
        self.__results = {}
     
      
    def __init_services__(self):
        for  impo, modname, data in pkgutil.iter_modules(services.__path__):
            logger.info("{0} {1} {2}".format(impo, modname, data))
            full_name = services.__name__ + '.' + modname
            imported_module = importlib.import_module(full_name)
            for name, obj in inspect.getmembers(imported_module):
                if inspect.isclass(obj) and str(obj).find('services') != -1:
                    self.__results[name.lower()] = obj()
                    
    
    def get(self):
        self.__init_services__()
        return self.__results