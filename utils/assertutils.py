'''
Created on 18-Jun-2021

@author: Abhishek Prajapati
'''

import re
from support.razor_logger import logger

def handle_assertion(f):
    def wrapper(self, actual, expected):
        try:
            return f(self,actual, expected)
        except AssertionError as w:
            logger.error(str(w))
            raise w
    return wrapper   


class AssertUtils(object):
    
    
    def __init__(self):
        self.__comparator = "equals"
        self.__actual_value = None
        self.__expected_value = None
    
    
    def __equals__(self, actual, expected):
        assert actual == expected, "Actual value: {0} is not equal to the expected value: {1}.".format(actual,expected)
        msg="Actual value: {0} is equal to the expected value: {1}.".format(actual,expected)
        logger.info(msg)
        return msg
      
    
    def __not_equals__(self, actual, expected):
        assert actual != expected, "Actual value: {0} is equal to the expected value: {1}.".format(actual,expected)
        msg = "Actual value: {0} is not equal to the expected value: {1}.".format(actual,expected)
        logger.info(msg)
        return msg
    
    def __greater_than__(self, actual, expected):
        assert actual > expected, "Actual value: {0} is not greater than expected value: {1}.".format(actual,expected)
        msg = "Actual value: {0} is greater than expected value: {1}.".format(actual,expected)
        logger.info(msg)
        return msg
     
   
    def __greater_than_equal__(self, actual, expected):
        assert actual >= expected, "Actual value: {0} is not greater than or equal to the expected value: {1}.".format(actual,expected)
        msg = "Actual value: {0} is greater than or equal to the expected value: {1}.".format(actual,expected)
        logger.info(msg)
        return msg
    
    def __less_than__(self, actual, expected):
        assert actual < expected, "Actual value: {0} is not less than the expected value: {1}.".format(actual,expected)
        msg = "Actual value: {0} is less than the expected value: {1}.".format(actual,expected)
        logger.info(msg)
        return msg
            
    def __less_than_equal__(self, actual, expected):
        assert actual <= expected, "Actual value: {0} is not less than or equal to the expected value: {1}.".format(actual,expected)
        msg = "Actual value: {0} is  less than or equal to the expected value: {1}.".format(actual,expected)
        logger.info(msg)
        return msg
        
    def __contains__(self, actual, expected):
        assert actual in expected, "Actual value: {0} is not present in the expected values: {1}.".format(actual,expected)
        msg = "Actual value: {0} is present in the expected values: {1}.".format(actual,expected)
        logger.info(msg)
        return msg
        
    def __not_contain__(self, actual, expected):
        assert actual not in expected, "Actual value: {0} is present in the expected values: {1}.".format(actual,expected)
        msg = "Actual value: {0} is not present in the expected values: {1}.".format(actual,expected)
        logger.info(msg)
        return msg
        
    def __matches__(self, actual, expected):
        assert bool(re.match(expected, actual)), "Actual value: {0} does not match with the expected value: {1}.".format(actual,expected)
        msg = "Actual value: {0} matches with the expected value: {1}.".format(actual,expected)
        logger.info(msg)
        return msg
                 
    def __does_not_match__(self, actual, expected):
        assert not bool(re.match(expected, actual)), "Actual value: {0} matches with the expected value: {1}.".format(actual,expected)
        msg = "Actual value: {0} does not match with the expected value: {1}.".format(actual,expected)
        logger.info(msg)
        return msg
    
    def __get_assert_method__(self, operator):
        return {
            
            "equals" : self.__equals__,
            "greater than" :  self.__greater_than__,
            "greater or equals" : self.__greater_than_equal__,
            "less than" : self.__less_than__,
            "less or equals" : self.__less_than_equal__,
            "not equal" : self.__not_equals__,
            "contains" : self.__contains__,
            "does not contain" : self.__not_contain__,
            "matches" : self.__matches__,
            "does not matches" : self.__does_not_match__
            
            }.get(operator.lower(), None)
        
                
    def assert_handler(self, operator, actual, expected):
        expected_operators = [ "equals", "greater than", "greater or equals", "less than", "less or equals" , "not equal", "contains", "does not contain", "matches", "does not matches"]
        if not operator == None or operator == '':
            self.__comparator = operator
            
        if self.__comparator not in expected_operators:
            raise ValueError("Unrecognized operator: {0}. Please use any of the following operator: {1}".format(operator, ','.join(expected_operators)))
        
        return self.__get_assert_method__(operator)(actual,expected) 
    
