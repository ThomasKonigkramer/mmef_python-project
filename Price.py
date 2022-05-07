"""
title : python project KMX Shipping Platform, Pricing Model

author: Sukanya Mukherjee

Pricing Model - we use this to present the three shipping method price options and to calculate the pre-tax and discount price.
"""

#we have to pip install tabulate and enum using " python3 -m pip install tabulate and python3 -m pip install enum" in the terminal.
#from re import L

from tabulate import tabulate
from enum import Enum


# import Order class

from Order import Package
from Order import Destination

#converting order output to be compatible to price input



class ShippingDetail:

    def __init__(self,  shipping_method, shipping_time, premium):
        self.shipping_method = shipping_method
        self.shipping_time = shipping_time
        self.premium = premium

priority = ShippingDetail('Priority', '1 day', 10)
express = ShippingDetail('Express', '2-3 days', 5)
standard = ShippingDetail('Standard', '5-6 days', 0)


baseprice = 8.0

class Price(Package,Destination):
   
    def __init__(self, _shipping_destination = 0, _package_size = 0, shipping_method = '', price = 0, time = 0):
        self._shipping_method = shipping_method
        self._shipping_destination = _shipping_destination
        self._package_size = _package_size
        self.price = price
        self.time = time

        #using setter method

        self._price = baseprice
        self._time = '0 days'
        Package.__init__(self,_package_size, shipping_method)
        Destination.__init__(self)
        
    #based on Order destination| setting it to a numeric value to use in Price
    def shipping_destination(self):
        if self.get_country_zone(self.country) == 'Domestic':
            self._shipping_destination = 1
        elif self.get_country_zone(self.country) == 'Rest of EU':
            self._shipping_destination = 1.25
        elif self.get_country_zone(self.country) == 'International':
            self._shipping_destination = 2
        return self._shipping_destination
    
    #based on Order Package | setting it to a numeric value to use in Price
    def packagesize(self):
      if self.get_package_size_category() == 'small':
         self._package_size = 1
      elif self.get_package_size_category() == 'medium':
         self._package_size = 1.75
      elif self.get_package_size_category() == 'big':
         self._package_size = 2
      return self._package_size
            
    def set_price(self, shipping_meth):
         if shipping_meth == priority.shipping_method:
            self.price = baseprice + 5*self.shipping_destination() + 2.5*self.packagesize() + priority.premium
         elif shipping_meth == express.shipping_method:
            self.price =  baseprice + 5*self.shipping_destination() + 2.5*self.packagesize() + express.premium
         elif shipping_meth == standard.shipping_method:
            self.price = baseprice + 5*self.shipping_destination() + 2.5*self.packagesize() + standard.premium
         return self.price
        
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
        return(tabulate([['1 --', 'Priority', '1 day', self.set_price(priority.shipping_method)], ['2 --', 'Express', '2-3 days', self.set_price(express.shipping_method)], ['3 --', 'Standard', '5-6 days', self.set_price(standard.shipping_method)]], headers=['Option', 'Service', 'Expected time', 'Price(€)']))

   # added this - tom
    def set_shipping_method(self, method):
       self.shipping_method = method


# example
if __name__ == '__main__':
    Sender1 = Destination('andy','BELGIUM')
    Sender1p = Package(4,2)
    print(Sender1)
    print(Sender1p)
    print(Destination.get_country_zone(Sender1,Sender1.country))
    Sender1PRICE = Price(Price.shipping_destination(Sender1),Price.packagesize(Sender1p),Price.get_shipping_method_category(Sender1p))

    print(Sender1PRICE.get_price_options())
    print(Sender1PRICE.set_price(Price.get_shipping_method_category(Sender1p)))
