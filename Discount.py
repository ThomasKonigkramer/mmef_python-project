"""
title : python project KMX Shipping Platform, Discounting

author: Sukanya Mukherjee

Discounts
"""

from traceback import print_last
from Price import Price

class Discount(Price):
    def __init__(self, discount, type, discountamount, discountedprice, shipping_method, _shipping_destination, _package_size, price, time):
        
        Price.__init__(self, shipping_method, _shipping_destination, _package_size, price, time)

        self.discount = discount
        self.type = type
        self.discountamount = discountamount
        self.discountedprice = discountedprice
       
        
        
    def set_discounting(self):
        if self.set_price(self._shipping_method) < 20:
            self.discountedprice = self.set_price(self._shipping_method)
        elif self.discount == True : 
            if self.type == "%":
                if self.discountamount <10 :
                    self.discountedprice = self.set_price(self._shipping_method)*(1 - self.discountamount/100)
                else :
                    return("Sorry! That is an invalid discount!")
            elif self.type =="flat":
                if self.discountamount <5 :
                    self.discountedprice = self.set_price(self._shipping_method) - self.discountamount
                else :
                    return("Sorry! That is an invalid discount!")   
            return(f'Congrats! Your new price is {self.discountedprice:.2f}. You have saved {self.price - self.discountedprice:.2f}')
        else :
            self.discountedprice = self.set_price(self._shipping_method) 
            return(f'Your price is {self.discountedprice:.2f}. You have not chosen a discount!')  
        
        
            
  
    def final_price(self):
        self.price = self.set_discounting()
        
"""import from user menu"""

user = Discount(False, "%",5,5,'Priority',2,2,0,0)
print(user.set_discounting())




