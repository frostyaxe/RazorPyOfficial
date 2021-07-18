import json

from jsonpath_ng import jsonpath, parse

json_data = json.load(open('report.json', 'rb'))

jsonpath_expression = parse('$.test-result.failed')

match = jsonpath_expression.find(json_data)

print(match)
