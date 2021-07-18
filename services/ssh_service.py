'''
Created on 11-Jul-2021

@author: Abhishek Prajapati
'''

# Importing requuired modules below
from razorpy_abstract.RazorPy import RazorPy
from paramiko import SSHClient,AutoAddPolicy, Transport, SFTPClient
from support.razor_logger import logger

class SSH(RazorPy):
    '''
        Description: This service allows the user to execute any command remotely via SSH.
        Author: Abhishek Prajapati (frostyaxe)
    '''
    
    def __init__(self):
        '''
            Description: This constructor initializes the instance variables with the default values.
            Author: Abhishek Prajapati (frostyaxe)
        '''
        self.__host = None
        self.__port = None
        self.__username = None
        self.__password = None
        self.__command = None
        self.__exec_type = "cmd"
        self.__method = "GET"
        self.__localpath = None
        self.__remotepath = None
    
    ####################  Getters ####################
    
    @property
    def host(self):
        return self.__host
    
    @property
    def port(self):
        return self.__port
    
    @property
    def username(self):
        return self.__username
    
    @property
    def password(self):
        return self.__password
    
    @property 
    def command(self):
        return self.__command
    
    @property
    def exec_type(self):
        return self.__exec_type
    
    @property
    def method(self):
        return self.__method
    
    @property
    def local_path(self):
        return self.__localpath
    
    @property
    def remote_path(self):
        return self.__remotepath
        
    
    ####################  Setters ####################
    
    @host.setter
    def host(self, host):
        self.__host = host
        
    @port.setter 
    def port(self, port):  
        self.__port = port
        
    @username.setter 
    def username(self, username):
        self.__username = username
        
    @password.setter 
    def password(self, password):
        self.__password = password
        
    @command.setter 
    def command(self,command):
        self.__command = command   
    
    @exec_type.setter
    def exec_type(self, exec_type):
        self.__exec_type = exec_type
    
    @method.setter
    def method(self, transfer_method):
        self.__method = transfer_method
    
    
    @local_path.setter
    def local_path(self, localpath):
        self.__localpath = localpath
        
    @remote_path.setter
    def remote_path(self, remotepath):
        self.__remotepath = remotepath
        
    
    def __execute_command__(self):
        
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(self.host, self.port, self.username, self.password)
        stdin, stdout, stderr = client.exec_command(self.command)  
        logger.info("[ {0} ] ".format(__name__) + " Sent command remotely using SSH")
        stdin.close()
        
        for line in stderr.readlines():
            message="[ Standard Error ] {0}".format(line)
            logger.error(message)
            
        return ''.join(stdout.readlines())
        
    def __file_transer__(self):
        
        
        transport = Transport((self.host,self.port))
        transport.connect(None,self.username,self.password)
        client = SFTPClient.from_transport(transport)
        
        try:
            if self.method.upper() == "GET":
                client.get(self.remote_path,self.local_path)
               
                return "File received from {0} to {1}".format(self.remote_path,self.local_path)
            elif self.method.upper() == "PUT":
                client.put(self.local_path,self.remote_path)
                return "File transferred from {0} to {1}".format(self.local_path,self.remote_path)
            else:
                raise ValueError("Unrecognized method: {0}. Valid values are GET and PUT".format(self.method))
        finally:
            
            logger.info("Closing FTP client")
            if client: client.close()
            logger.info("Closing Transport")
            if transport: transport.close()
            
        
    def execute(self):
        
        logger.info("[ {0} ] ".format(__name__) + " Initiating execution using SSH service.")
        
        if self.exec_type.lower() == "cmd":
            return self.__execute_command__()
        elif self.__exec_type.lower() == "file transfer":
            return self.__file_transer__()
            

        
        
        
        
