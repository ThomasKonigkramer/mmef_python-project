"""
title : python project KMX Shipping Platform, Discounting

author: Sukanya Mukherjee

Discounts
"""

from Price import Price

class Discount(Price):
    def __init__(self, discount, type, discountamount = 0, discountedprice = 0, _shipping_destination = 0, _package_size = 0, shipping_method = '', price = 0, time = 0):
        
        Price.__init__(self, shipping_method, _shipping_destination, _package_size, price, time)

        self.discount = discount
        self.type = type
        self.discountamount = discountamount
        self.discountedprice = discountedprice
       
        
    def set_discounting(self):
        if self.set_price(self._shipping_method) < 20:
           return ("Minimum purchase of 20€ required to avail discount") 
        else : 
            if self.discount == True and self.type == "%":
                if self.discountamount in range(1,10,1) :
                    self.discountedprice = self.set_price(self._shipping_method)*(1 - self.discountamount/100)
                    return(f'Congrats! Your new price is {self.discountedprice:.2f} €. You have saved {self.price - self.discountedprice:.2f} €!')  
                else :
                    return("Sorry! That is an invalid discount. Your price remains the same.")
            elif self.discount == True and self.type =="flat":
                if self.discountamount in range(1,5,1) :
                    self.discountedprice = self.set_price(self._shipping_method) - self.discountamount
                    return(f'Congrats! Your new price is {self.discountedprice:.2f} €. You have saved {self.price - self.discountedprice:.2f} €!')  
                else :
                    return("Sorry! That is an invalid discount. Your price remains the same.")   
            else :
                self.discountedprice = self.set_price(self._shipping_method)
                return(f'Your  price remains the same at {self.discountedprice:.2f} €.')    
  
    def final_price(self):
        self.price = self.set_discounting()
        
"""import from user menu"""
if __name__ == '__main__':
    user = Discount(True, "%",5,5,'Priority',2,2,21,0)
    print(user.set_discounting())




