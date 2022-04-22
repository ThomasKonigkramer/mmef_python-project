"""
title : python project KMX Shipping Platform, Pricing Model

author: Sukanya Mukherjee

Pricing Model - we use this to present the three shipping method price options and to calculate the pre-tax and discount price.
"""
#import order

distance_code = 2 #range circles 1 to 5
shipping_method = 1.5 #Priority(1.5) /Express(1) /Standard (0)"
shipping_destination = 1 #"Domestic- EU(0)/International(1)"
package_size = 1.5 #Small 0/ Medium 1/ Big 1.5"
fragile = 1 #is it fragile?

baseprice = 8

"""price pre VAT/discounts"""

class Price:
    def __init__(self, shipping_method, shipping_destination,package_size,distance_code):
        self.shipping_method = shipping_method
        self.shipping_destination = shipping_destination
        self.package_size = package_size
        self.distance_code = distance_code

    def get_price(self):
         if self.shipping_method == "Priority":
            price = baseprice + 5*shipping_destination + 2.5*package_size + 2.5*distance_code + 5
         elif self.shipping_method == "Express":
            price =  baseprice + 5*shipping_destination + 2.5*package_size + 2.5*distance_code + 2.5
         elif self.shipping_method == "Standard":
            price = price = baseprice + 5*shipping_destination + 2.5*package_size + 2.5*distance_code

    def get_price_options(self):
        from tabulate import tabulate
        print(tabulate([['Priority', '24 hours',24], ['Express','2-3 days', 19],['Standard','5-6 days', 19]], headers=['Service', 'Expected time', 'Price']))


user = Price("")