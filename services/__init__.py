from flask import Flask,render_template
from jinja2 import Environment, FileSystemLoader
from threading import Thread, Timer
from managers import vars_manager
from os import path
from managers import exec_details_manager

app = Flask(__name__)
user_vars = {}
@app.route("/", methods=["POST", "GET"])
def home():
            
        file_loader = FileSystemLoader(path.join(vars_manager.AppsVars.PROJECT_ROOT_DIR ,'templates'))
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True
        
        template = env.get_template('dashboard.tpl')
        
        output = template.render(execution_details=exec_details_manager.execution_details,razor_status=exec_details_manager.razor_status)
        return output

def run():
    app.run()

#   Preparing parameters for flask to be given in the thread
#   so that it doesn't collide with main thread
host = "127.0.0.1"
port = 5000
kwargs = {'host': host, 'port': port, 'threaded': False, 'use_reloader': False, 'debug': False}
import webbrowser
Timer(1.25, lambda: webbrowser.open('http:///{0}:{1}'.format(host,port)) ).start()
flaskThread = Thread(target=app.run, kwargs=kwargs)
flaskThread.daemon = True
flaskThread.start()