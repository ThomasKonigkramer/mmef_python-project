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
    def get_name(self):
        return self.name
    name = input('Name:')
    while len(name) == 0:
        name = input('please enter your Name:')
    if len(name) != 0:
        print(name)
    def get_phonenumber(self):
     return self.phonenumber
    phonenumber = input('phonenumber:')
    if len(phonenumber) == 10:
       print(phonenumber)
    else:
        phonenumber = input('please enter the correct phonenumber:')
    def get_country(self):
        return self.country
    country = input('country:')
    country = str.upper(country)
    if country == 'FRANCE':
        print(country)
    else:
        print('we do not suopport the service yet')
    def get_city(self):
        return self.city
    city = input('city:')
    print(city)
    def get_address(self, address):
        return self.address
    address = input('address:')
    print(address)
    def get_code(self,code):
        return self.code
    code = input('code:')
    print(code)
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

    def get_name(self):
        return self.name
    name = input('Name:')
    while len(name) == 0:
        name = input('please enter your Name:')
    if len(name) != 0:
        print(name)
    def get_phonenumber(self):
        return self.phonenumber
    phonenumber = input('phonenumber(+0):')
    while len(phonenumber) != 10:
        phonenumber = input('please enter the correct phonenumber:')
    if len(phonenumber) == 10:
        print(phonenumber)

def get_country(country):
    zone1 = ['FRANCE']
    zone2 = ['AUSTRIA, BELGIUM, BULGARIA, CROATIA, REPUBLIC OF CYPRUS, CZECH REPUBLIC, DENMARK, ESTONIA, FINLAND, GERMANY, GREECE, HUNGARY, IRELAND, ITALY, LATVIA, LITHUANIA, LUXEMBOURG, MALTA, NETHERLANDS, POLAND, PORTUGAL, ROMANIA, SLOVAKIA, SLOVENIA, SPAIN, SWEDEN']
    country = str.upper(country)
    if country in zone1:
        return 'Domestic'
    elif country in zone2:
        return 'European'
    else:
        return 'International'
country = input('country:')
print(get_country(country))


def get_city(self):
    return self.city

    city = input('city:')
    print(city)

def get_address(self, address):
    return self.address
    address = input('address:')
    print(address)

    def get_code(self, code):
        return self.code

    code = input('code:')
    print(code)

class Package:
    def __init__(self, weight, shippingmethod):
        self.weight = weight
        self.service = service

    def __str__(self):
        return f'the weight is {self.weight}, the service is {self.service}'

    def get_weight(self):
        if weight <= 1:
            return ('small')
        elif weight > 1 and weight <= 3:
            return ('medium')
        elif weight >= 4:
            return ('big')
        elif weight >= 10:
            return ('it is too big to delivery')
    weight = input('weight:')
    weight = int(weight)
def get_shippingmethod(self):
    if shippingmethod == 1:
        return 'Priority'
    elif shippingmethod == 2:
        return 'Express'
    else:
        shippingmethod == 3
        return 'Standard'
shippingmethod = input('please choose( 1:Priority 2:Express 3:Standard):')
shippingmethod = int(shippingmethod)
#














