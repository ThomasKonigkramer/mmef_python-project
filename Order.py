# #title : python project - KMX Shipping Platform, new order class
# #    author : Xiao JIANG
# ## place a new order ### only focus on delivery from france
# # Demand analysis to get the price throuth the address and size
# #first to get the distance of the delivery

print('where are you shipping from:')
class From:
    def __init__(self, name, phonenumber, country, city, address, code):
        self.name = name
        self.phonenumber = phonenumber
        self.country = 'France'
        self.city = city
        self.address = address
        self.code = code
    def __str__(self):
        return f'Name: {self.name}, phonenumber: {self.phonenumber}, country:{self.country}, city:{self.city}' \
               f'Address:{self.address}, Code.__{self.code}'
    def name(self):
        while len(name) == 0:
            return False
        if len(name) != 0:
            return name
    def phonenumber(self):
        if len(phonenumber) == 10:
            return phonenumber
        else:
            return False
    def country(self):
        if country == 'FRANCE':
            return country
        else:
            return 'we do not suopport the service yet'
    def city(self):
        return self.city
    def address(self, address):
        return self.address
    def code(self,code):
        return self.code
# example
Sender1 = From('andy', 1234567890,'france','paris','qwert', 12345)
print(Sender1)

class Destination:
    def __init__(self, name, phonenumber, country, address, code):
        self.name = name
        self.phonenumber = phonenumber
        self.country = 'France'
        self.city = city
        self.address = address
        self.code = code

    def __str__(self):
        return f'Name: {self.name}, phonenumber: {self.phonenumber}, country:{self.country}, city:{self.city}' \
               f'Address:{self.address}, Code.__{self.code}'

    def name(self):
         while len(name) == 0:
             return self.name
         if len(name) != 0:
             return False
    def phonenumber(self):
         while len(phonenumber) != 10:
             return False
         if len(phonenumber) == 10:
            return self.phonenumber
    #check if this is ok, what is getting returned? change this to 
    def set_country(self, country):
        zone1 = ['FRANCE']
        zone2 = ['AUSTRIA, BELGIUM, BULGARIA, CROATIA, REPUBLIC OF CYPRUS, CZECH REPUBLIC, DENMARK, ESTONIA, FINLAND, GERMANY, GREECE, HUNGARY, IRELAND, ITALY, LATVIA, LITHUANIA, LUXEMBOURG, MALTA, NETHERLANDS, POLAND, PORTUGAL, ROMANIA, SLOVAKIA, SLOVENIA, SPAIN, SWEDEN']
        country = str.upper(country)
        if country in zone1:
            return 'Domestic'
        elif country in zone2:
            return 'Rest of EU'
        else:
            return 'International'
        
    def city(self):
        return self.city

    def address(self, address):
        return self.address

    def code(self, code):
            return self.code

class Package:
    def __init__(self, package_size, shipping_method):
        self.package_size = package_size
        self.shipping_method = shipping_method

    def __str__(self):
        return f'the package_size is {self.package_size}, the service is {self.shipping_method}'

    def package_size(self):
        if self.package_size <= 1:
            return ('small')
        elif self.package_size > 1 and self.package_size <= 3:
            return ('medium')
        elif self.package_size >= 4:
            return ('big')
        elif self.package_size >= 10:
            return ('Sorry! it is too big to deliver!')
#perhaps change to names directly
    def shipping_method(self):
        if shipping_method == 1:
            return 'Priority'
        elif shipping_method == 2:
            return 'Express'
        else:
            shipping_method == 3
            return 'Standard'


user = Package(2,'Priority')
print(user.shipping_method)

