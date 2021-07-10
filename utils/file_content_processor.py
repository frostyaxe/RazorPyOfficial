'''
Created on 18-Jun-2021

@author: Abhishek Prajapati
'''
from pyexception.RazorException import RazorException
import elementpath
from jsonpath_ng import parse



def xml_content_processor(root, input_vars, dictionary,result_dictionary):
    
    for var_key in input_vars:
        if var_key in dictionary:
            result_list = elementpath.select(root, dictionary[var_key])
            print ("Original list for key - {0} is : ".format(var_key) + str(result_list)) 
            if var_key not in result_dictionary:
                result_dictionary[var_key] = sum(list(map(int, result_list)))
            else:
                result_dictionary.update({var_key : result_dictionary[var_key] + sum(list(map(int, result_list)))})
    
        else:
            raise RazorException(RazorException.DATAMISSING + " PLease provide the pattern for key: {0} defined in process pattern using dictionary.".format(var_key))
            print(" PLease provide the pattern for key: {0} defined in process pattern using dictionary.".format(var_key))
            exit(1)
    return result_dictionary
    
                    
def json_content_processor(json_obj, input_vars, dictionary,result_dictionary):   
    def results(data):
        return [ result.value for result in data ]
    
    for var_key in input_vars:
        if var_key in dictionary:
            jsonpath_expression = parse(dictionary[var_key])
            result_list = jsonpath_expression.find(json_obj)
            if var_key not in result_dictionary:
                result_dictionary[var_key] = sum(list(map(int, results(result_list))))
            else:
                result_dictionary.update({var_key : result_dictionary[var_key] + sum(list(map(int, results(result_list))))})
            
            print(result_list[0].value)
        else:
            raise RazorException(RazorException.DATAMISSING + " PLease provide the pattern for key: {0} defined in process pattern using dictionary.".format(var_key))
            print(" PLease provide the pattern for key: {0} defined in process pattern using dictionary.".format(var_key))
            exit(1)    
    return result_dictionary       