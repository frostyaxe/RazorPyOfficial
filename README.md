# RazorPy
RazorPy deals with the activities related to the DevOps process. User needs to create a yaml file based on that this application performs the required actions.

Currently this application supports below services.
- apitest
- cowsay
- email
- gating
- html
- python
- template
- url

</br>

## Services

### apitest: 
This service allows you to test the rest APIs. It uses validators to validate the data returned by the rest API url upon execution.

YAML Example:
```sh
    - apitest:
         name: "Working with the rest API get requests" 
         base_url: "https://reqres.in"
         api_path: "api/users"
         query_param: 
             page: "{{ page_no }}"
         authentication:
              scheme : "bearer"
              token : "<token>"
         headers:
             - "Content-Type" : "application/json"
         response_type: "json"
         request:
             method: "POST"
             payload: "{'name':'Abhishek', 'gender':'Male', 'email':'abhishek@15ce.com', 'status':'Active'}"
         vars:
            page_no: 2
         capture:
             type: 'var'
             name: 'rest_response'
         validators:
             expected_status:
                  - 200
                  
             compare:
                  - json_path: "$.total_pages"
                    comparator: "equals"
                    expected: 2
```

| Key | Description |
| ------ | ------ |
| name | Any fancy name to distinguish this task in between multiple tasks |
| base_url |  A base URL is, basically, the consistent part of your web address |
| api_path | Endpoint path of the rest URL |
| query_param | Query parameters that are attached to the end of a url. Here key will be your query parameter key and value will be the value for that parameter |
| headers | Request header to provide information about the request context. Request headers must be specified in the key value pair. You can add as many headers you want based on the requirement. |
|request|Help you specify request method as well as payload. Currently it supports only GET, PUT, POST and DELETE as request methods.|
|authentication|Currently it accepts two authentication scheme, basic and token. In order to provide bearer token for authentication, you need to specify the token in "token" key and if the authentication scheme is basic then you will have to provide credentials details in "username" and "password" key.|
| response_type | Type of the response in which data should be returned. Valid values for this key are json and xml |
| vars | User defined parameters that can be used in the execution of task from YAML. |
| capture | To capture the output of the task execution either in the console of variable. <br /> <ul><li> type: Valid values for this key is "console" and "var". By default it will display the output in console else you can redirect the output into any variable by specifying variable name in the "name" key and type as "var".</li></ul> |
| validators | To specify the details required for the validation of the response data. <ul><li><b>expected_status:</b> You can specify the expected response statuses in the form of list. If actual response status code matches with any of the expected statuses then it will pass the assertion. </li> <li><b>compare:</b> It stores the data related for performing the validations on the retrieved response data. You can specify details many times in the form of list for multiple validations. For the validation of JSON content, you need to use "json_path". In case of xml response, you need to use "xml_path". Supported <i>comparators</i> are "equals", "greater than", "greater or equals", "less than", "less or equals" , "not equal", "contains", "does not contain", "matches" and "does not matches. The value that you are expecting must be provided in the <i>expected</i> section."</li></ul> |
</ br>

### cowsay: 
This service allows you to generate ASCII art pictures of a cow or any other character with a message. Supported characters are 'beavis', 'cheese', 'daemon', 'cow', 'dragon', 'ghostbusters', 'kitty', 'meow', 'milk', 'pig', 'stegosaurus', 'stimpy', 'trex', 'turkey', 'turtle' and 'tux'.

YAML Example:
```sh
    - cowsay:
         name: "Displaying Message in Tux"
         character: "tux"
         message: "Hello, World"
```

| Key | Description |
|-----|------|
| character | Allows you to change the character of which ASCII art picture is going to get generated |
| message | Any text message to be displayed with the generated ASCII art picture |

</br>

### email: 
This service allows you to send the emails with attachments based on the requirements to the specified recipients automatically.

YAML Example:
```sh
 - email:
          sender: "<sender username>@gmail.com"
          password: "<secret_key>"
          recipient: "<recipient1 username>@gmail.com,<recipient2 username>@gmail.com"
          subject: "RazorPy Email Service Test"
          attachments:
                 - "razor.yml"
                 - "output.html"
          smtp:
              host: "smtp.gmail.com"
              port: 465    
          body:
              string: "<html><body><img src='cid:testimage' /><br>{{mail_body}}</body></html>"    
                 
          vars:
             mail_body: "<b>Hello Abhishek Here,</b><br><br> This is the auto-generated mail. Please do not reply unless you wanna get spammed! <br><br> <b>Thanks,</b><br>Abhishek Prajapati." 

```

| Key | Description |
|------|------|
| sender | Sender email ID |
| password | Secret key(password) of the sender email ID for the authentication |
| recipient | Recipient email IDs. Multiple email IDs are separated by comma |
| subject | Subject for the automated email |
| attachments | This section is optional. If you want to send the attachment then only specify the detail otherwise remove it from YAML content |
| smtp | Allows you to specify the details related to the SMTP server |
| body | Mail body string. Here you can use jinja syntax as well to make this mail string more dynamic. Currently it supports only string. In the future, it will support the file templates for mail body too |
| vars | User defined parameters |

</br>

### gating: 
This service allows you to abort the execution based on the certain conditions. You can read any kind of json and xml reports and based on that you can specify the failure threshold in percentage. It failure rate exceeds more than the specified threshold then it will abort the current execution else it will proceed normally for the further execution. It is mostly used with the selenium test execution where you receive some surefire reports or cucumber reports. You can specify the details of those reports and based on the requirement, you can set the threshold.

YAML Example:

1. For xml report processing:
```sh
- gating:
        filter: ".*.xml"  
        report_dir: "D:\\Downloads"  
        process_pattern: "{%raw%} {{failure}}/{{total}}*100 {% endraw %}"
        process_type: 'xml'
        dictionary:
            failure : '//testng-results/@failed'
            total: '//testng-results/@total'
        threshold: 75
        
```

2. For json report processing:
```sh
- gating:
        filter: ".*.json"  
        report_dir: "E:\\Abhishek\\Eclipse Projects\\RazorPy\\others"  
        process_pattern: "{%raw%} {{failure}}/{{total}}*100 {% endraw %}"
        process_type: 'json'
        dictionary:
            failure : '$.test-result[*].failed'
            total: '$.test-result[*].total'
        threshold: 27

```

| key | description |
|------|------|
| filter | Allows you to filter out the files that are going to be included in the further processing |
| report_dir| Allows you to specify the directory location in which report files exist |
| process_pattern | This pattern allows you to how to process the required details fetched from the report files. It must always start with {%raw%} and end with {%endraw%}. Between those prefix and suffix you can specify the mathetical operation that you need to perform in order to calculate the percentage that will be verified with the specifed threshold later on |
| process_type | Based on what files are you going to process, you need to specify the value. Valid values are json and xml  |
| dictionary | This section allows you to specify the either json path or xml path based on the process type you have selected. Here key will be the variable name in which retrieved data will be stored in our case, "failure" and "total" are keys in which data will be stored. |
| threshold | Failure threshold in the percentage |


</br>

### html: 
This service allows you to create an html page using the html components that this framework supports. Currently it supports only table and alert component but the development of the other components is in progress.

YAML Example:

```sh
- html:
          file: "output.html"
          components:
              - table:
                  headings: 
                      - name
                      - age
                  rows:
                     - "Abhishek, 27"
                     - "Vinit, 70"
                     - "Pawan, 90"
                     - "korean, 21"
                  attribs:
                      component: 
                           class: "table"
                      header:
                           class: "thead-dark"
          
              - alert:
                   title: "Exception Found:"
                   message: "Error occured @line 27."
                   enableClose: "false"  
                   attribs:
                        class: "alert-success"  
```

|key|Description|
|-----|-----|
|file| Name of the output html file|
|components|Details related to the components that you want to display on the html page|

Please find the details for the components below:

Table:

|Key|Description|
|-----|------|
|headings|Column Header in the list format|
|rows|Data to be displayed in a row. All the cell data must be separated by comma|
|attribs|Bootstrap classes can be used in order to manipulate the appearance of the component|
|header| This will help to change the appearance of the table header|

Alert:
|Key|Description|
|------|------|
|title|Title to be displayed on the alert box|
|message| Message to be displayed on the alert box|
|enableClose| This allows you choose whether you want to display the close button for the alert message or not|
|attribs| This allows you to specify the desired attributes for the component|

</br>

### python: 
This service allows you to execute or evaluate the python statement or expression in the string format.

YAML Example:
```sh
- python:
         type: "exec"
         string: "print(message)"
         vars:
             message: "Hello, Abhishek Prajapati"    
- python:
         type: 'eval'
         string: '10//2'
```

|Key|Description|
|-----|-----|
|type|By default, the type of the execution will exec. If you want to evaluate the python expression in string format then provide "eval" as a value to this key. <\br> <ul><li>exec: This executes the python statements specified in the string.</li><li>eval: This evaluates the python expression in the string.</li></ul>|
|string| Specify the python statement or python expression in string format|

</br>

### template: 
This service allows you to generate the configuration file based on the template provided either in the string format or file.

YAML Example:

```sh

- template:
         name: "Example of jinja2 templating."
         string: "{% raw %} Hello Abhishek {{ message }} {% endraw %}. I am coming from local vars : {{zombie}} .Response: {{rest_response}}" 
         vars:
             zombie: "Abhishek Prajapati"

 - template:
         name: "Example of jinja2 templating."
         file: "others/base.txt"
         vars:
             name: "Abhishek Prajapati"

```

|Key|Description|
|------|------|
|string|Jinja2 template string|
|file|Jinja2 template file|

</br>

### url: 
This service allows you to execute any rest API call. It returns the response in desired format either text, xml or json. Downloading the files using rest api is still in progress.

YAML Example:

```sh

    - url:
         name: "Working with the rest API post requests" 
         base_url: "https://gorest.co.in"
         api_path: "public-api/users" 
         query_param:
             key1: "val1"
         authentication:
              scheme : "bearer"
              token : "<token>"
         request:
             method: "POST"
             payload: "{'name':'Abhishek', 'gender':'Male', 'email':'abhishek@15ce.com', 'status':'Active'}"
         headers:
             - "Content-Type" : "application/json"
         response_type: "text"    
         
```

| Key | Description |
| ------ | ------ |
| name | Any fancy name to distinguish this task in between multiple tasks |
| base_url |  A base URL is, basically, the consistent part of your web address |
| api_path | Endpoint path of the rest URL |
|authentication|Currently it accepts two authentication scheme, basic and token. In order to provide bearer token for authentication, you need to specify the token in "token" key and if the authentication scheme is basic then you will have to provide credentials details in "username" and "password" key.|
| query_param | Query parameters that are attached to the end of a url. Here key will be your query parameter key and value will be the value for that parameter |
| headers | Request header to provide information about the request context. Request headers must be specified in the key value pair. You can add as many headers you want based on the requirement. |
|request|Help you specify request method as well as payload. Currently it supports only GET, PUT, POST and DELETE as request methods.|
| response_type | Type of the response in which data should be returned. Valid values for this key are json and xml |

</br>
</br>

## Reporting
Once the execution is completed, this framework generates the html report as shown in the below image.

![Report](https://github.com/frostyaxe/RazorPy/blob/master/others/report.PNG?raw=true)

## Prerequisite
REQUIRED Python 3.9

## Usage
In order to initiate the execution of instructions that are written in the YAML file, you need to execute the command as shown below.
<b>Syntax:</b>
```sh
python application.py -f <yml file name>
```
<i>Command:</i>
```sh
python application.py -f razor.yml
```

## Author
* Abhishek Prajapati ( prajapatiabhishek1996@gmail.com )

###### Note: Suggestions are always welcome. If you feel anything needs to be added to make this application better. Please feel free to drop me an email @ prajapatiabhishek1996@gmail.com
