'''
Created on 21-Feb-2021

@author: Abhishek Prajapati
'''
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import smtplib, ssl

from jinja2 import Template

from pyexception.RazorException import RazorException
from razorpy_abstract.RazorPy import RazorPy


class Email(RazorPy):
    
    def __init__(self):
        self.__sender_email = None
        self.__receiver_email = None
        self.__password = None
        self.__subject = None
        self.__html = None
        self.__smtp = None
        self.__body = None
        self.__razor_vars = None
        self.__attachments = None
        
    @property
    def sender(self):
        return self.__sender_email
    
    
    @sender.setter
    def sender(self, sender):
        self.__sender_email = sender
        
    @property
    def recipient(self):
        return self.__receiver_email
    
    @recipient.setter
    def recipient(self, recipient):
        self.__receiver_email = recipient
        
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, password):
        self.__password = password
        
    @property
    def subject(self):
        return self.__subject
    
    @subject.setter
    def subject(self, subject):
        self.__subject = subject
    
    @property
    def smtp(self):
        return self.__smtp
    
    @smtp.setter
    def smtp(self, smtp):
        self.__smtp = smtp
        
    @property
    def body(self):
        return self.__body
    
    @body.setter
    def body(self, body):
        self.__body = body
        
    @property
    def razor_vars(self):
        return self.__razor_vars
    
    @razor_vars.setter
    def razor_vars(self, razor_vars):
        self.__razor_vars = razor_vars
        
    @property
    def attachments(self):
        return self.__attachments
    
    @attachments.setter 
    def attachments(self, attachments):
        self.__attachments = attachments     
    
    def __get_smtp_connection_details(self): 
        
        if self.smtp == None:
            raise RazorException(RazorException.DATAMISSING + "Please provide the data related to smtp in Razorpy Yaml file. " )
            exit(1)
            
        if not "host" in self.smtp:
            raise RazorException(RazorException.DATAMISSING + "Host value is missing in the smtp details.")
            exit(1)
            
        if not "port" in self.smtp:
            raise RazorException(RazorException.DATAMISSING + "Port value is missing in the smtp details.")
            exit(1)   
        
        smtp_host = self.smtp['host']
        smtp_port = self.smtp['port']
          
        return smtp_host,smtp_port
     
     
    def __add_attachments(self, message, attach_file_name):
        
        ctype, encoding = mimetypes.guess_type(attach_file_name)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        
        maintype, subtype = ctype.split("/", 1)
        
        if maintype == "text":
            fp = open(attach_file_name)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(attach_file_name, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(attach_file_name, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(attach_file_name, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=attach_file_name)
        message.attach(attachment)
               
    def execute(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.sender
        message["To"] = self.recipient
        
        mail_body = None
        if "string" in self.body:
            body_string = self.body['string']
            try:
                template = Template(body_string)
                mail_body = template.render(self.razor_vars.user_vars)
            except TypeError as type_err_obj:
                if str(type_err_obj).lower().find("can't compile non template nodes") == -1:
                    raise TypeError(str(type_err_obj))
        else:
            raise RazorException(RazorException.INVALIDDATA + "Invalid mail body type. Either string or file must be defined in the RazorPy YML.")
            exit(1)

        mail_part = MIMEText(str(mail_body), "html")
        img = MIMEImage(open("email_header.png",'rb').read(), 'png')
        img.add_header('Content-Id', '<testimage>')
        message.attach(img)
       
        message.attach(mail_part)
        
        for attachment in self.attachments:
            self.__add_attachments(message, attachment)
        
        smtp_host, smtp_port = self.__get_smtp_connection_details()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(str(smtp_host), int(smtp_port), context=context) as server:
            server.login( str(self.sender),  str(self.password))
            server.sendmail(self.sender,  self.recipient.split(','), message.as_string()) 

        return "Mail is sent to the following recipients -----> {0}".format(self.recipient)
            
