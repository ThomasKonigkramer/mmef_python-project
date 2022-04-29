"""
title: python project - KMX Shipping Platform, main module

authors:        Thomas Konigkramer  

1 -- databases
2 -- printing and formating
3 -- user prompts and information validation
4 -- menues

Version 1       User sign-in/sign-up; dynamic options menu; dynamic prompt menues; database set-up for customers and paymentcards
Version 2       function:      
"""

'''importing python packages'''
import pandas as pd
import getpass
import os
from datetime import datetime

'''importing custom classes and modules'''
import Customers
import PaymentCards
import Price
import Discount
import Order

###################################################################################################
'''
database and custom classes functions
'''

'''retrieve database information'''

def get_dbdirectory(db):
    '''
    db - customers or paymentcards
    returns directory of db
    '''
    working_dir = os.getcwd()
    db_dir = working_dir + '\database'
    
    if db == 'customers':
        customers_dir = db_dir + '\db_customers.csv'
        return customers_dir
    elif db == 'paymentcards':
        paymentcards_dir = db_dir + '\db_paymentcards.csv'
        return paymentcards_dir
    elif db == 'orders':
        orders_dir = db_dir + '\db_orders.csv'
        return orders_dir

def get_dbasdf(db):
    '''
    get db as df
    db - customers or paymentcards
    returns df of db
    '''
    if db == 'customers':
        customers_dir = get_dbdirectory('customers')
        df_customers = pd.read_csv(customers_dir)
        return df_customers
    elif db == 'paymentcards':
        paymentcards_dir = get_dbdirectory('paymentcards') 
        df_paymentcards = pd.read_csv(paymentcards_dir)  
        return df_paymentcards
    elif db == 'orders':
        orders_dir = get_dbdirectory('orders')
        df_orders = pd.read_csv(orders_dir)
        return df_orders
    else:
        return ''


def id_format(id):
    '''
    db_s.csv stores user_id as integer, but is a 9 digit code, with leading zeros
    converts number from db to have leading zeros
    '''
    return str(id).rjust(9,'0')


def retrieve_list_from_db(df, item):
    '''
    function that retrieves lists of column values in csv database 
    parameters: database - dataframe of csv file. Of form df_name
                item - column name we want in list
    '''
    if item == "User_id":
        retrieved_list = df[item].to_list()
        for i in range(len(retrieved_list)):
            retrieved_list[i] = id_format(retrieved_list[i])
    else:
        retrieved_list = df[item].to_list()
    
    return retrieved_list


def call_customer_from_db(identifier, use_username = True):
    '''
    creates a Customer instance using unique username or user_id identifier
    which it queries from database
    parameters  :   identifier - either username or user_id of existing customer
                    use_username - True if provided username, False if provided user_id
                    df - defaults to df_customers, but wouldn't work for other df
    '''   
    df = get_dbasdf('customers')
    if use_username is True:
        row = df[df['Username']==identifier]
        username = identifier
        user_id = id_format(row['User_id'].iloc[0])
    else:
        identifier = int(identifier)
        row = df[df['User_id']==identifier]
        username = row['Username'].iloc[0]
        user_id = id_format(identifier)

    firstname = row['Name'].iloc[0]
    surname = row['Surname'].iloc[0]
    password = row['Password'].iloc[0]

    customer = Customers.Customers(firstname, surname, username, user_id, password)

    return customer


def call_paymentcards_from_db(customer):
    '''
    returns list of paymentcards belonging to user
    '''
    username = customer.get_username()
    df = get_dbasdf('paymentcards')
    cards_df = df[df['Username']==username]
    cards_list = cards_df.values.tolist()

    firstname = customer.get_firstname()
    surname = customer.get_surname()
    user_id = customer.get_userid()
    password = customer.get_password()
    paymentcards = []
    for card in cards_list:
        paymentcard = PaymentCards.PaymentCards(firstname, surname, username, user_id, password)
        paymentcard.set_card_number(card[1])
        paymentcard.set_expiry_date(card[2])
        paymentcard.set_card_balance(card[3])
        paymentcards.append(paymentcard)

    return paymentcards



# paymentcards = call_paymentcards_from_db('jimmy')
# for card in paymentcards:
#     print(card)

# call_customer_from_db('jimmy')


def sort_paymentcards(customer):
    '''
    returns list of paymentcard instances
    '''
    paymentcards = call_paymentcards_from_db(customer)
    for card in paymentcards:
        if card.is_expired() == True:
            paymentcards.remove(card)
        if card.get_card_balance() == 0:
            paymentcards.remove(card)

    # for card in paymentcards:
    #     print(card.get_expiry_date())
    paymentcards.sort(key = lambda x: x.get_datetime_expiry())
    # for card in paymentcards:
    #     print(card.get_expiry_date())
   
    return paymentcards
    



customer = call_customer_from_db('jimmy')
sort_paymentcards(customer)

def in_db(instance, db):
    '''
    checks whether an instance has been added to a database, using a unique identifier
    returns true (1) or false (0)
    '''

def modify_db(instance, db):
    '''
    modify db - takes class and updates relevant csv
    parameters: instance - is a module (customer, paymentcard, etc.)
                db - name of database to write to
    '''
    dir = get_dbdirectory(db)
    df = get_dbasdf(db)
    column_names = list(df)
    if db == 'customers':      
        customer_details = instance.get_detailslist()
        df_newcustomer = pd.DataFrame([customer_details], columns = column_names)
        df = pd.concat([df, df_newcustomer], ignore_index = False)
        df.to_csv(dir, index = False)
    
    elif db == 'paymentcards':
        card_numbers = retrieve_list_from_db(df, 'Card_number')
        # print(card_numbers)
        card_details = instance.get_card_details()
        if instance.get_card_number() in card_numbers:
            # print(instance.get_card_number())
            # df.replace(to_replace=)
            # print(instance.get_card_balance())
            df.loc[df['Card_number']==instance.get_card_number(), 'Card_balance'] = instance.get_card_balance()
            df.to_csv(dir, index = False)
            # df['Card_balance'] = df[df['Card_number']==instance.get_card_number()]['Card_balance']=instance.get_card_balance()
        else:            
            df_newcard = pd.DataFrame([card_details], columns = column_names)
            df = pd.concat([df, df_newcard], ignore_index = False)
            df.to_csv(dir, index = False)
    elif db == 'orders':
        order_details = instance.get_order_details_list()
        df_neworder = pd.DataFrame([order_details], columns = column_names)
        df = pd.concat([df, df_neworder], ignore_index = False)
        df.to_csv(dir, index = False)

def find_max_id(id_list):
    '''
    function for version user and tracking ids
    '''
    max_id = 0
    for ids in id_list:
        ids = int(ids)
        if ids > max_id:
            max_id = ids
    # temporarily string instead of integer in db, but causes no issues
    new_id = id_format(max_id + 1)
    return new_id


###################################################################################################
'''
printing/formating functions
'''


def print_bars():
    '''
    printing functions used to enhance display
    '''
    print('----------------------------------------------------------------------------------------')


def print_welcome_menu():
    '''
    printing function - welcome menu
    '''
    print_bars()
    print('Welcome to the KMX Shipping Platform.')
    print('This is the login menu.')
    print('1 -- Sign-in : existing customer')
    print('2 -- Sign-up : new customer')
    print('3 -- Exit')
    print_bars()


def print_username_or_id():
    '''
    printing function
    '''
    print_bars()
    print('Login details:')
    print('1 -- Username')
    print('2 -- User ID')
    print('3 -- Return to main menu')
    print_bars()


def print_customer_menu():
    '''
    printing function - customer menu
    '''
    print_bars()
    print('This is the customer menu.')
    print('1 -- Place a new order')
    print('2 -- View orders in progress')
    print('3 -- View order history')
    print('4 -- Add gift-card or payment-card')
    print('5 -- View my gift-card/payment-card balances')
    print('6 -- Return to main menu')
    print_bars()


def print_shipping_method():
    '''
    printing function - shipping method options
    '''
    print_bars()
    print('These are the shipping method options:')
    print('1 -- Priority')
    print('2 -- Express')
    print('3 -- Standard')
    print('4 -- Return to main menu')
    print_bars()

def print_discount_menu():
    '''
    printing function - is discount flat or percentage
    '''
    print_bars()
    print('1 -- Percentage discount')
    print('2 -- Flat discount')
    print('3 -- Return to main menu')
    print_bars()

def print_payment_menu():
    '''
    printing function - payment menu
    '''
    print_bars()
    print('This is the payment menu.')
    print('1 -- Pay by cash')
    print('2 -- Pay by gift-card/payment-card')
    print('3 -- Cancel order and return to main menu')
    print_bars()


###################################################################################################
'''
functions used for option menus and prompts from users
'''
    
def option_menu(menu):
    '''
    function used when providing option to user and requiring choice
    parameters: menu - dictionary
    description of menu dictionaries
        0 : printing function name
        1 - n : list of actions to perform, either strings or parameterless functions,
                or integers used in menu selection
    '''
    no_options = len(menu)
    while True:
        # printing function called
        menu.get(0)()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print_bars()
            print('Input incorrect - please enter a number.')
        if option == 1:
            # list under menu_dic item 1
            for action in menu.get(1):
                if type(action) == str:
                    print(action)
                elif type(action) == int:
                    return action
                else: # paramterless function
                    action()
        # loop over 2->n items in menu_dic
        for i in range(2, no_options):
            if option == i:
                # since values are lists of actions
                actions = menu.get(i)
                for action in actions:
                    if type(action) == str:
                        print(action)
                    elif type(action) == int:
                        return action
                    else: # parameterless function
                        action()
        else:
            print_bars()
            print(f'Invalid option. Please enter a number between 1 and {no_options-1}.')


def info_prompt_check(request, requests = [], is_signup = True):
    # def info_prompt_check(request, requests = [], is_signup = True, back_to = ''):
    '''
    function to receive new information, check against database, and return to previous menu
    parameters: request - information requested from user
                requests - database list to check information against
                is_signup - defaults to T, is F when getting new information
                back_to - return to last menu if incorrect information provided 3 times
    '''
    count = 0
    while(True):
        print_bars()
        try:
            prompt = input(f'{request}: ')
            if request == 'User_id':
                prompt = id_format(prompt)
        except:
            print_bars()
            print('Invalid information provided.')
        # check if list is not empty
        if requests:
            if is_signup is True:
                if prompt in requests and count < 2:
                    count += 1
                    print_bars()
                    print(f'{request} already exists - please choose a different one.')
                elif prompt in requests and count == 2:
                    print_bars()
                    print(f'{request} provided invalid. 3 attempts failed.')
                    main() # added after below
                else:
                    return prompt
            else:
                if prompt in requests and count <= 2:
                    return prompt
                elif prompt not in requests and count == 2:
                    print_bars()
                    print(f'{request} provided invalid. 3 attempts failed.')
                    main()
                else:
                    count += 1
                    print_bars()
                    print(f'{request} provided not valid - please try again.')
                    # print(request)
                    # print(requests)
        else:
            return prompt


def info_prompt_hidden(request, requests = []):
    # def info_prompt_hidden(request, requests = [], back_to = ''):
    '''
    function to receive hidden information from users, e.g. passwords
    parameters:     request - the information we require from the user
                    requests - is non empty list when we want this to be unique information
                    back_to - last menu you may want to return to
    '''
    count = 0
    while(True):
        print_bars()
        try:
            prompt = getpass.getpass(f'{request}: ')
        except:
            print_bars()
            print('Invalid information provided.')
        # check if list is not empty
        if requests:
            if prompt == requests and count <= 2:
                print_bars()
                print(f'{request} correct.')
                return prompt
            elif count == 2:
                print_bars()
                print(f'{request} provided invalid. 3 attempts failed.')
                main() # added
            else:
                count += 1
                print_bars()
                print(f'{request} provided incorrect')
        elif not requests:
            print_bars()
            check = getpass.getpass(f'Please confirm your {request}: ')
            if prompt != check:
                print_bars()
                print("Your entries don't match - please try again.")
            else:
                return prompt


###################################################################################################
'''
menu functions
'''

def welcome_menu():
    '''
    welcome menu steps: asks user whether signing in or signing up
    returns customer instance
    '''
    welcome_menu_dic = { # see form under option_menu()
        0 : print_welcome_menu,
        1 : [1], # signin
        2 : [2], # signup
        3 : [print_bars, 
        'Thank you for visiting the KMX Shipping Platfrom. Enjoy your day.',
        print_bars,
        exit]
    }

    next_menu = option_menu(welcome_menu_dic)

    if next_menu == 1: 
        customer = signin_menu()
    elif next_menu == 2:
        customer = signup_menu()
    
    return customer


def signin_menu():
    '''
    function for user signin menu
    requests username and password from user
    returns customer instance
    '''
    print_bars()
    print('Signing back in:')

    df = get_dbasdf('customers')

    signin_menu_dic = { # see form under option_menu()
        0 : print_username_or_id,
        1 : [1], # username
        2 : [2], # user id
        3 : [print_bars, 
        'Returning to Welcome menu.',
        print_bars,
        main]
    }
    unique_identifier = option_menu(signin_menu_dic)
    if unique_identifier == 1:
        usernames = retrieve_list_from_db(df, 'Username')
        username = info_prompt_check('Username', usernames, False)
        # username = info_prompt_check('Username', usernames, False, 'signin')
        customer = call_customer_from_db(username)
    elif unique_identifier == 2:
        user_ids = retrieve_list_from_db(df, 'User_id')
        user_id = info_prompt_check('User_id', user_ids, False)
        # user_id = info_prompt_check('User_id', user_ids, False, 'signin')
        customer = call_customer_from_db(user_id, False)
        username = customer.get_username()
    
    check_password = customer.get_password()

    password = info_prompt_hidden('Password', check_password)
    # password = info_prompt_hidden('Password', check_password, 'welcome')
    print_bars()
    print(f'Welcome back, {username} !')
    print(customer)
    
    return customer


def signup_menu():
    '''
    menu for new customer signup to get information necessary for customer class
    returns customer instance
    '''
    df = get_dbasdf('customers')
    usernames = retrieve_list_from_db(df, 'Username')
    firstname = info_prompt_check('Name')
    surname = info_prompt_check('Surname')
    username = info_prompt_check('Username', usernames, True)
    # username = info_prompt_check('Username', usernames, True, 'welcome')
    password = info_prompt_hidden('Password')
 
    user_ids = retrieve_list_from_db(df, 'User_id')
    
    user_id = find_max_id(user_ids)
    
    customer = Customers.Customers(firstname, surname, username, user_id, password)
    
    modify_db(customer, 'customers')

    print_bars()
    print(f'Welcome, {username} !')
    print(customer)

    return customer


def customer_menu(customer):
    '''
    customer menu steps: ask what user wants to do
    returns order instance or displays requested information
    '''

    customer_menu_dic = {
    0 : print_customer_menu,
    1 : [1], # new order
    2 : [2], # orders in progress
    3 : [3], # order history
    4 : [4], # view payment cards
    5 : [5], # add gift card/payment card
    6 : [print_bars, 
        'Thank you for visiting the KMX Shipping Platfrom. Enjoy your day.',
        print_bars,
        main]
    }

    next_menu = option_menu(customer_menu_dic)

    if next_menu == 1:
        order = new_order(customer)
        paying = payment(order)
    elif next_menu == 2:
        print('Orders in progress')
        print('This feature is currently not available.')
        print('Returning to customer menu')
        customer_menu(customer)
    elif next_menu == 3:
        print('Order history')
        print('This feature is currently not available.')
        print('Returning to customer menu')
        customer_menu(customer)
    elif next_menu == 4:
        print('Add gift card/payment card')
        new_card = new_paymentcard(customer)
        print('New card has been created')
        print('Returning to customer menu')
        customer_menu(customer)
    elif next_menu == 5:
        print('View payment cards:')
        paymentcards = call_paymentcards_from_db(customer)
        if paymentcards == []:
            print_bars()
            print(f'{customer.get_username()} does not have any gift-cards/payment-cards')
        for card in paymentcards:
            print(card)
        customer_menu(customer)
        

def new_order(customer):
    '''
    this function makes use of the Order, Price and Discount classes to create and price a new order
    returns order instance
    '''
    print_bars()
    print(f'Creating new order for {customer.get_firstname()} {customer.get_surname()}')


    print_bars()
    print('Requesting sender information:')
    sender_details = Order.From()

    name = info_prompt_check("Sender's Full Name")
    while sender_details.set_name(name) != None:
        print_bars()
        print(sender_details.set_name(name))
        name = info_prompt_check("Sender's Full Name")
    
    country = info_prompt_check('Sender Country')
    while sender_details.set_country(country) != None:
        print_bars()
        print(sender_details.set_country(country))
        country = info_prompt_check('Sender Country')


    print_bars()
    print('Requesting receiver information:')
    receiver_details = Order.Destination()
    
    name = info_prompt_check("Receiver's Full Name")
    while receiver_details.set_name(name) != None:
        print_bars()
        print(receiver_details.set_name(name))
        name = info_prompt_check("Receiver's Full Name")
    
    country = info_prompt_check('Destination Country')
    while receiver_details.set_country(country) != None:
        print_bars()
        print(receiver_details.set_country(country))
        country = info_prompt_check('Destination Country')


    print_bars()
    print('Requesting package details:')
    package_details = Order.Package()

    weight = info_prompt_check("Package's weight (kg)")
    while package_details.set_package_size(weight) != None:
        print_bars()
        print(package_details.set_package_size(weight))
        weight = info_prompt_check("Package's weight (kg)")

    ## pricing ##
    print_bars()
    package_weight = package_details.get_package_size()
    destination = receiver_details.get_country_zone(receiver_details.get_country())
    package_category = package_details.get_package_size()
    price = Price.Price(destination, package_category, package_weight)
    price.shipping_destination() # to convert
    price.packagesize() # to convert
    print(price.get_price_options()) # options 
    shipping_method_dir = {
        0 : print_bars,
        1 : [1],
        2 : [2],
        3 : [3]
    }

    shipping_method = option_menu(shipping_method_dir)
    
    package_details.set_shipping_method(shipping_method) # set after seeing effect on price
    shipping_method_cat = package_details.get_shipping_method_category() # convert

    price.set_time(shipping_method_cat) # setting time to delivery
    price.set_price(shipping_method_cat) # setting price chosen

    print_bars()
    print('Checking if you have a valid discount:')

    is_discount = True # would include some code/check - excluded in this project
    
    discount_menu_dir = {
        0 : print_discount_menu,
        1 : [1],
        2 : [2],
        3 : [print_bars,
        'Returning to Welcome menu.',
        print_bars,
        main]
    }
    
    flat_or_perc = option_menu(discount_menu_dir)

    if flat_or_perc == 1:
        flat_or_perc = '%'
    else:
        flat_or_perc = 'flat'

    disc_rate = int(info_prompt_check('Flat/percentage discount rate'))

    price_shipping = price._shipping_method
    # print(price_shipping)
    price_destination = price._shipping_destination
    # print(price_destination)
    price_pack_size = price._package_size
    # print(price_pack_size)
    
    discounting = Discount.Discount(is_discount, flat_or_perc, disc_rate, price_shipping, price_destination, price_pack_size, package_details.get_package_size(), price.price, price.time)
    
    print(discounting.set_discounting())
    # print(discounting.price)
    # print(discounting.discountedprice)

    if discounting.discountedprice == 0:
        final_price = discounting.price
    else:
        final_price = discounting.discountedprice

    # create order instance
    today = datetime.now().date().strftime("%d/%m/%y") # order date
    order = Order.Order(customer, final_price, today)

    df = get_dbasdf('orders')

    tracking_ids = retrieve_list_from_db(df, 'Tracking_number')
    # print(tracking_ids)
    tracking_id = find_max_id(tracking_ids)

    order.set_tracking_id(tracking_id)

    return order



def new_paymentcard(customer):
    '''
    returns list of paymentcard instances
    '''
    firstname = customer.get_firstname()
    surname = customer.get_surname()
    username = customer.get_username()
    user_id = customer.get_userid()
    password = customer.get_password()

    new_card = PaymentCards.PaymentCards(firstname, surname, username, user_id, password)

    card_number = info_prompt_check('Card number')
    while new_card.set_card_number(card_number) != None:
        print_bars()
        print(new_card.set_card_number(card_number))
        card_number = info_prompt_check('Card number')

    expiry_date = info_prompt_check('Expiry date')
    while new_card.set_expiry_date(expiry_date) != None:
        print_bars()
        print(new_card.set_expiry_date(expiry_date))
        expiry_date = info_prompt_check('Expiry date')
    
    card_balance = info_prompt_check('Card balance')
    while new_card.set_card_balance(card_balance) != None:
        print_bars()
        print(new_card.set_card_balance(card_balance))
        card_balance = info_prompt_check('Card balance')

    modify_db(new_card, 'paymentcards')

    return new_card

# customer1 = call_customer_from_db('zo')
# cards = sort_paymentcards(customer1)
# cost = 7500

# for card in cards:
#     cost = card.withdraw(cost) 
#     print(card) 
#     modify_db(card, 'paymentcards')
#     # print(cost) 

# print(f'{cost} of the total cost remains to be paid in cash.')

def payment(order):
    print_bars()
    print('Proceeding to payment - how will you pay:')

    payment_menu_dir = {
        0 : print_payment_menu,
        1 : [1], # cash
        2 : [2],  # gift card
        3 : [print_bars, 
        'Returning to Welcome menu.',
        print_bars,
        main]
    }

    payment_method = option_menu(payment_menu_dir)

    if payment_method == 1:
        print_bars()
        print('You are paying by cash - thank you very much')
        modify_db(order, 'orders')
        print(order)
    else:
        print_bars()
        print('You are paying by gift-card/payment-card')
        modify_db(order, 'orders')
        cards = sort_paymentcards(customer)
        cost = order.get_price() #order.discountprice

        for card in cards:
            cost = card.withdraw(cost) 
            # print(card) 
            modify_db(card, 'paymentcards')
        
        if cost > 0:
            print_bars()
            print(f'{cost} of the total cost remains to be paid in cash.')
        else:
            print_bars()
            print('Your gift-cards/payment-cards paid the entirety of the delivery cost.')
        # print(order)


# customer1 = call_customer_from_db('jimmy')
# order1 = new_order(customer1)
# print(order1)


def main():
    customer = welcome_menu()

    customer_action = customer_menu(customer)

    print_bars()
    print('Thank you for visiting the KMX Shipping Platfrom. Logging you off.')

    main()

###################################################################################################    


main()



# customer1 = call_customer_from_db('jimmy')
# sender1 = Order.From('Bob Davis', 'France')
# # print(sender1.country)
# receiver1 = Order.Destination('Charley Man', 'South Africa')
# package1 = Order.Package(3,1)
# # shipping_method_4th = 1/2/3
# discount1 = Discount.Discount(True, 'flat', 5, package1.get_shipping_method(), receiver1.get_country(), package1.get_package_size(), 30, '1 day',29)
# today = datetime.now().date().strftime("%d/%m/%y")
# # print(today)

# order1 = Order.Order(customer1, sender1, receiver1, package1, discount1, today, 3)

# test = order1.get_order_details_list()
# # print(test)

# sender2 = order1.get_sender()
# print(sender2.get_country())