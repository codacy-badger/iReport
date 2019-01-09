from flask import json
import datetime


class User:
    """class for user registration"""

    def __init__(self, user_id, firstname, lastname, othernames, username, email, phone_number, password, isAdmin):
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.othernames = othernames
        self.username = username
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        self.registered_on = datetime.datetime.now()

    def __str__(self):
        return "user: {} firstname:{} lastname:{} othernames:{} username:{} phonenumber:{} with email {}:isadmin:{}".format(self.user_id ,self.firstname,self.lastname,self.othernames,self.username,
        self.phone_number,self.email, self.isAdmin)


class Redflag:
    """
    class for creating a redflag post 
    """

    def __init__(self, redflag_id, user_id, description, email, location, createdby, createdOn):
        self.redflag_id = redflag_id
        self.user_id = user_id
        self.description = description
        self.email = email
        self.status = self.status()[0]
        self.location = location
        self.createdOn =  datetime.datetime.now()
        self.createdby = createdby
        
    def __str__(self):
        return "redflag_id:{} user_id:{} description:{} email:{} location:{} createdby:{} createdOn:{} status:{} ".format(self.user_id,self.redflag_id,self.description,self.email,self.location,self.createdOn, self.createdby, self.status)

    # def status(self):
    #     """
    #     show status list for redflag posted
    #     """
    #     status = ['received','rejected', 'under_investigation', 'resolved', 'on-going']
    #     return status




