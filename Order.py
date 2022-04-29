# #title : python project - KMX Shipping Platform, new order class
# #    author : Xiao JIANG
# ## place a new order ### only focus on delivery from france
# # Demand analysis to get the price throuth the address and size
# #first to get the distance of the delivery

# print('where are you shipping from:')
import time

class From:

    def __init__(self, name = '', country = '', phonenumber = 0000000000, city = '-', address= '-', code='-'):
        self.name = name
        self.phonenumber = phonenumber
        self.country = country
        self.city = city
        self.address = address
        self.code = code
    
    def __str__(self):
        return f'Name: {self.name}, phonenumber: {self.phonenumber}, country: {self.country}, city: {self.city}, ' \
               f'Address: {self.address}, Code: {self.code}'
    # changed to set
    def set_name(self, name):
        if len(name) == 0:
            return "Please enter the sender's full name"
        else:
            self.name = name

    # edit: changed name and parameters        
    def set_country(self, country):
        country = country.upper() # added
        if country == 'FRANCE':
            self.country = country
        else:
            return 'We currently only support orders sent from France.'

    def get_country(self):
        return self.country

    def get_name(self):
        return self.name

    def city(self):
        return self.city
    def address(self, address):
        return self.address
    def code(self,code):
        return self.code

    def phonenumber(self):
        if len(self.phonenumber) == 10:
            return self.phonenumber
        else:
            return False

class Destination:
    def __init__(self, name = '', country = '', phonenumber = 0000000000, city = '-', address= '-', code='-'):
        self.name = name
        self.phonenumber = phonenumber
        self.country = country
        self.city = city
        self.address = address
        self.code = code

    def __str__(self):
        return f'Name: {self.name}, phonenumber: {self.phonenumber}, country: {self.country}, city: {self.city}, ' \
               f'Address: {self.address}, Code: {self.code}'

    # def name(self):
    #      while len(self.name) == 0:
    #          return self.name
    #      if len(self.name) != 0:
    #          return False

    def set_name(self, name):
        if len(name) == 0:
            return "Please enter the sender's full name"
        else:
            self.name = name

    def set_country(self, country):
        self.country = country

    def phonenumber(self):
         while len(self.phonenumber) != 10:
             return False
         if len(self.phonenumber) == 10:
            return self.phonenumber
    #check if this is ok, what is getting returned? change this to 
    def get_country_zone(self, country):
        zone1 = ['FRANCE']
        zone2 = ['AUSTRIA, BELGIUM, BULGARIA, CROATIA, REPUBLIC OF CYPRUS, CZECH REPUBLIC, DENMARK, ESTONIA, FINLAND, GERMANY, GREECE, HUNGARY, IRELAND, ITALY, LATVIA, LITHUANIA, LUXEMBOURG, MALTA, NETHERLANDS, POLAND, PORTUGAL, ROMANIA, SLOVAKIA, SLOVENIA, SPAIN, SWEDEN']
        country = str.upper(country)
        if country in zone1:
            return 'Domestic'
        elif country in zone2:
            return 'Rest of EU'
        else:
            return 'International'

    def get_country(self):
        return self.country
        
    def city(self):
        return self.city

    def address(self, address):
        return self.address

    def code(self, code):
            return self.code

class Package:
    def __init__(self, package_size = 0, shipping_method = 1):
        self._package_size = package_size
        self._shipping_method = shipping_method

    def __str__(self):
        return f'the package_size is {self._package_size}, the service is {self._shipping_method}'

    # def package_size(self):
    #     if self._package_size <= 3:
    #         return ('small')
    #     elif self._package_size > 3 and self._package_size <= 10:
    #         return ('medium')
    #     elif self._package_size >= 10 and self._package_size <=20:
    #         return ('big')
    #     elif self._package_size >= 20:
    #         return ('Sorry! It is too big for us to deliver!')

    # added this
    def set_package_size(self, weight):
        try:
            int(weight)
        except ValueError:
            return 'Must provide a number'
        weight = int(weight)
        if weight < 0:
            return 'Cannot have a negative weight'
        elif weight > 20:
            return 'Maximum package weight is 20 kg'
        else:
            self._package_size = int(weight)
    
    def get_package_size(self):
        return self._package_size

    # added this
    def set_shipping_method(self, method):
        if method in [1,2,3]:
            self._shipping_method = method
        else:
            return 'Not a valid option'

    def get_package_size_category(self):
        if self._package_size <= 3:
            return ('small')
        elif self._package_size > 3 and self._package_size <= 10:
            return ('medium')
        elif self._package_size >= 10 and self._package_size <=20:
            return ('big')
        elif self._package_size >= 20:
            return ('Sorry! It is too big for us to deliver!')
            
    #perhaps change to names directly
    def get_shipping_method_category(self):
        if self._shipping_method== 1:
            return 'Priority'
        elif self._shipping_method == 2:
            return 'Express'
        else:
            self._shipping_method == 3
            return 'Standard'

    def get_shipping_method(self):
        return self._shipping_method

class Order:

    def __init__(self, customer, price, date, delivery_preference = 0, tracking_id = 0):
        self.__customer = customer
        self.__price = price
        self.__date = date
        self.__delivery_preference = delivery_preference
        self.__tracking_id = tracking_id

    def get_delivery_preference(self):
        return self.__delivery_preference

    def set_delivery_preference(self, preference):
        if preference == 1: # home delivery (0 default for depot delivery)
            self.__price += 2
        self.__delivery_preference = preference

    def get_customer(self):
        return self.__customer

    def get_price(self):
        return self.__price
    
    def get_date(self):
        return self.__date

    def get_tracking_id(self):
        return self.__tracking_id

    def set_order_code(self):
        #year/month/date/hour/minute/second+time.time and 7 more
        order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(time.time()).replace('.', '')[-7:])
        self.__tracking_id = order_no

    def get_order_code(self):
        return self.__tracking_id

    def get_order_details_list(self):
        username = self.__customer.get_username()
        return [username, self.__price, self.__date, self.__delivery_preference, self.__tracking_id]

    # def get_delivery_date(self):

    def __str__(self):
        return f'Your order has been completed. Tracking number: {self.__tracking_id}'





#test sukanya
if __name__ == '__main__':
    # example
    Sender1 = From('andy', 1234567890,'france','paris','qwert', 12345)
    print(Sender1)

    user = Package(24)
    print(user)

