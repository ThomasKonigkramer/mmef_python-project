"""
title : python project KMX Shipping Platform, Pricing Model

author: Sukanya Mukherjee

Pricing Model - we use this to present the three shipping method price options and to calculate the pre-tax and discount price.
"""

#we have to pip install tabulate and enum using " python3 -m pip install tabulate and python3 -m pip install enum" in the terminal.
from tabulate import tabulate
from enum import Enum


# from order import Package


#converting order output to be clcompatible to price input



class ShippingDetail:

    shipping_method = ''
    shipping_time = ''
    premium = 0.0

    def __init__(self,  shipping_method, shipping_time, premium):
        self.shipping_method = shipping_method
        self.shipping_time = shipping_time
        self.premium = premium


priority = ShippingDetail('Priority', '1 day', 5)
express = ShippingDetail('Express', '2-3 days', 2.5)
standard = ShippingDetail('Standard', '5-6 days', 0)


baseprice = 8.0

"""price pre VAT/discounts"""

class Price:

    def __init__(self, shipping_method, shipping_destination, package_size, distance_code, price, time):
        self.shipping_method = shipping_method
        self.shipping_destination = shipping_destination
        self.package_size = package_size
        self.distance_code = distance_code
        self.price = price
        self.time = time

        #using setter method

        self._price = baseprice
        self._time = '0 days'

    def set_price(self, shipping_meth):
         if shipping_meth == priority.shipping_method:
            self._price = baseprice + 5*self.shipping_destination + 2.5*self.package_size + 2.5*self.distance_code + priority.premium
         elif shipping_meth == express.shipping_method:
            self._price =  baseprice + 5*self.shipping_destination + 2.5*self.package_size + 2.5*self.distance_code + express.premium
         elif shipping_meth == standard.shipping_method:
            self._price = baseprice + 5*self.shipping_destination + 2.5*self.package_size + 2.5*self.distance_code
         return self._price
        
    def set_time(self, shipping_meth):
        if shipping_meth == priority.shipping_method:
            self._time = priority.shipping_time
        elif shipping_meth == standard.shipping_method:
            self._time = standard.shipping_time    
        elif shipping_meth == express.shipping_method:
            self._time = express.shipping_time
        return self._time
    
    def get_time()

    def get_price_options(self):
        print("Your price options are :")
        print('')
        return(tabulate([['Priority', '1 day', self.set_price(priority.shipping_method)], ['Express', '2-3 days', self.set_price(express.shipping_method)], ['Standard', '5-6 days', self.set_price(standard.shipping_method)]], headers=['Service', 'Expected time', 'Price(€)']))


"""test"""

user = Price("Standard", 1, 1.5, 2, 0, 0)


print('\nYour price is ', user.set_price(user.shipping_method), "€ and you will get your delivery in ", user.set_time(user.shipping_method),"!Be there soon!")

print(user.get_price_options())
