"""
title : python project KMX Shipping Platform, Discounting

author: Sukanya Mukherjee

Discounts
"""

import Price

class Discount(Price.Price):
    def __init__(self, price, discount, type, discountedamount, discountedprice):
        
        super().__init__(price)

        self.discount = discount
        self.type = type
        self.discountedamount = discountedamount
        self.discountedprice = discountedprice
        
        

    def set_discounting(self):
        if self.price < 20:
           return ("Minimum purchase of 20€ required to avail discount") 
        else : 
            if self.discount == True and self.type == "%":
                if self.discountedamount <10 :
                    self.discountedprice = self.discountedprice*(1 - self.discountedamount)
                else :
                    return("Sorry! That is an invalid discount")
            elif self.discount == True and self.type =="flat":
                if self.discountedamount <5 :
                    self.discountedprice = self.discountedprice - self.discountedamount
                else :
                    return("Sorry! That is an invalid discount")   
            else :
                self.discountedprice = self.price
        return("Congrats! Your new price is", self.discountedprice,". You have saved", self.price - self.discountedprice,".")
        
"""import from user menu"""

user = Discount(5,True, "%",5,5)
user.discountedprice





