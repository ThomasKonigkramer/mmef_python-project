"""
title: python project - KMX Shipping Platform, Customers class

authors:        Thomas Konigkramer  

Customer class
"""

class Customers:
    '''
    A class to handle a customer's attributes
    '''

    def __init__(self, firstname, surname, username, user_id, password):
        self.__firstname = firstname
        self.__surname = surname
        self.__username = username
        self.__password = password
        self.__user_id = user_id

    def __str__(self):
        bars = '----------------------------------------------------------------------------------------\n'
        summary_message = bars + f'User details:\nUser ID     : {self.__user_id}\nUsername    : {self.__username}\nFirst name  : {self.__firstname}\nSurname     : {self.__surname}'
        return summary_message

    def get_firstname(self):
        return self.__firstname

    def get_surname(self):
        return self.__surname
    
    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_userid(self):
        return self.__user_id
    
    def get_detailslist(self):
        return [self.__user_id, self.__firstname, self.__surname, self.__username, self.__password]


