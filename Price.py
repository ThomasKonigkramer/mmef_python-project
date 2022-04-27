"""
title : python project KMX Shipping Platform, Pricing Model

author: Sukanya Mukherjee

Pricing Model - we use this to present the three shipping method price options and to calculate the pre-tax and discount price.
"""

#we have to pip install tabulate and enum using " python3 -m pip install tabulate and python3 -m pip install enum" in the terminal.
from re import L
from tabulate import tabulate
from enum import Enum


# from order import Package

import Order

#converting order output to be clcompatible to price input



class ShippingDetail:

    shipping_method = ''
    shipping_time = ''
    premium = 0.0

    def __init__(self,  shipping_method, shipping_time, premium):
        self.shipping_method = shipping_method
        self.shipping_time = shipping_time
        self.premium = premium


priority = ShippingDetail('Priority', '1 day', 10)
express = ShippingDetail('Express', '2-3 days', 5)
standard = ShippingDetail('Standard', '5-6 days', 0)


baseprice = 8.0

"""price pre discounts"""



class Price:

    def __init__(self, shipping_method, shipping_destination, package_size, price, time):
        self.shipping_method = shipping_method
        self._shipping_destination = shipping_destination
        self._package_size = package_size
        self.price = price
        self.time = time

        #using setter method

        self._price = baseprice
        self._time = '0 days'
    
    #based on Order destination| setting it to a numeric value to use in Price
    def shipping_destination(self):
        if Order.Destination.set_country() == 'Domestic':
            self._shipping_destination = 1
        elif Order.Destination.set_country() == 'Rest of EU':
            self._shipping_destination = 1.25
        elif Order.Destination.set_country() == 'International':
            self._shipping_destination = 2
    
    #based on Order Package | setting it to a numeric value to use in Price
    def package_size(self):
        if Order.Package.package_size() == 'small':
            self._package_size = 1
        elif Order.Package.package_size() == 'medium':
            self._package_size = 1.25
        elif Order.Package.package_size() == 'big':
            self._package_size = 2
            
    def set_price(self, shipping_meth):
         if shipping_meth == priority.shipping_method:
            self._price = baseprice + 5*self.shipping_destination + 2.5*self.package_size + priority.premium
         elif shipping_meth == express.shipping_method:
            self._price =  baseprice + 5*self.shipping_destination + 2.5*self.package_size + express.premium
         elif shipping_meth == standard.shipping_method:
            self._price = baseprice + 5*self.shipping_destination + 2.5*self.package_size 
         return self._price
        
    def set_time(self, shipping_meth):
        if shipping_meth == priority.shipping_method:
            self._time = priority.shipping_time
        elif shipping_meth == standard.shipping_method:
            self._time = standard.shipping_time    
        elif shipping_meth == express.shipping_method:
            self._time = express.shipping_time
        return self._time
    
    def get_time(self):
        return self.set_time

    def get_price_options(self):
        print("Your price options are :")
        print('')
        return(tabulate([['Priority', '1 day', self.set_price(priority.shipping_method)], ['Express', '2-3 days', self.set_price(express.shipping_method)], ['Standard', '5-6 days', self.set_price(standard.shipping_method)]], headers=['Service', 'Expected time', 'Price(€)']))


"""test"""

user = Price("Standard", 1, 1.5, 2, 0)
print(user.set_price(user.shipping_method))
print('\nYour price is ', user.set_price(user.shipping_method), "€ and you will get your delivery in ", user.set_time(user.shipping_method),"!Be there soon!")

print(user.get_price_options())
