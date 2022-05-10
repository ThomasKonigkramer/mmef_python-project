"""
title: python project - KMX Shipping Platform, PaymentCards class

authors:        Thomas Konigkramer  

PaymentCards class
"""

'''importing python packages'''
from datetime import datetime
import re

'''importing parent classes'''
import Customers


class PaymentCards(Customers.Customers):
    '''
    A class to handle gift cards/payment cards
    '''

    def __init__(self, firstname, surname, username, user_id, password, card_number = 0, expiry_date = '', card_balance = 0):
        super().__init__(firstname, surname, username, user_id, password)
        self.__card_number = card_number
        self.__expiry_date = expiry_date
        self.__card_balance = card_balance


    def __str__(self):
        bars = '----------------------------------------------------------------------------------------\n'
        summary_message = bars + f'User details:\nUser ID     : {self.user_id}\nUsername    : {self.username}\nFirst name  : {self.firstname}\nSurname     : {self.surname}\nCard number : {self.__card_number}\nExpiry date : {self.__expiry_date}\nCard balance: {self.__card_balance}'
        return summary_message


    def set_card_number(self, number):
        if check_valid_number(number) == True:
            self.__card_number = number
        else:
           return f'Card number provided not in a valid format: ####/####/####' 


    def set_expiry_date(self, date):
        if check_date_valid(date) == True:
            self.__expiry_date = date
        else:
            return f'Date provided not in a valid format: dd/mm/yy'


    def set_card_balance(self, amount):
        try:
            int(amount)
        except ValueError:
            return 'Must provide a number'
        amount = int(amount)
        if amount <= 0:
            return f'Expecting a positive number for the card balance'
        else:
            self.__card_balance = amount


    def get_cardholder(self):
        cardholder_name = self.firstname + ' ' + self.surname
        return cardholder_name


    def get_card_number(self):
        return self.__card_number

    def get_card_balance(self):
        return self.__card_balance


    def get_expiry_date(self):
        return self.__expiry_date
    
    def get_datetime_expiry(self):
        date = self.__expiry_date
        day, month, year = date.split('/')
        return datetime(int(year), int(month), int(day))


    def withdraw(self, amount):
        # Cannot withdraw: amount is greater than balance
        remaining_cost = amount - self.__card_balance
        if remaining_cost < 0:
            remaining_cost = 0
        if amount <= self.__card_balance:
            self.__card_balance -= amount
        else:
            self.__card_balance = 0
        return remaining_cost

    def is_expired(self):
        # Card is expired and credited amounts are lost.
        today = datetime.now().date()
        day, month, year = self.__expiry_date.split('/')
        expiry = datetime(int(year), int(month), int(day)).date()
        if expiry > today:
            return 1
        # f'Card expiry not reached. Balance of {self.card_balance} remaining and valid until {self.expiry_date}.
        else:
            return 0
    
    def get_card_details(self):
        return [self.username, self.__card_number, self.__expiry_date, self.__card_balance]


def check_date_valid(date):
    '''
    returns true or false depending on whether the date provided is valid (true) or not (false)
    '''
    if re.search(r'\d{2}/\d{2}/\d{2}', date) and len(date)==8:
        day, month, year = date.split('/')
    else:
        return False
    try:
        datetime(int(year), int(month), int(day))
        return True
    except ValueError:
        return False


def check_valid_number(number):
    '''
    returns true or false depending on whether the card number provided is valid (true) or not (false)
    '''
    if re.match(r'\d{4}/\d{4}/\d{4}', number):
        return True
    else:
        return False

###################################################################################################
'''testing'''

if __name__ == '__main__':
    card1 = PaymentCards('Alex', 'Tester', 'tester', '000000003', 'test')
    expiry_set = card1.set_expiry_date('01/01/22')
    if expiry_set != None:
        print(expiry_set)
    balance_set = card1.set_card_balance(500)
    # if balance_set != None:
    #     print(balance_set)
    # print(card1)
    # number_set = card1.set_card_number('1111/1111/1111')
    # if number_set != None:
    #     print(number_set)
    # card1.withdraw(300)
    print(card1)

