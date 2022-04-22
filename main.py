"""
title: python project - KMX Shipping Platform, main module

authors:        Thomas Konigkramer  

1 -- databases
2 -- printing and formating
3 -- user prompts and information validation
4 -- menues
"""

'''importing python packages'''
import pandas as pd
import getpass
import os
from datetime import datetime

'''importing custom classes and modules'''
import Customers
import PaymentCards
# import Price
# import Discount

###################################################################################################
'''
database functions
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
    elif db == '':
           # orders_dir = db_dir + '\db_orders.csv'
        # paymentcards_dir = db_dir + '\db_paymentcards.csv'
        # promocodes_dir = db_dir + '\db_promocodes.csv'
        # df_packages = pd.read_csv(orders_dir)
        # df_paymentcards = pd.read_csv(paymentcards_dir) 
        # df_promocodes = pd.read_csv(promocodes_dir)
        return ''


def user_id_format(user_id):
    '''
    db_customers.csv stores user_id as integer, but is a 9 digit code, with leading zeros
    converts number from db to have leading zeros
    '''
    return str(user_id).rjust(9,'0')


def retrieve_list_from_db(df, item):
    '''
    function that retrieves lists of column values in csv database 
    parameters: database - dataframe of csv file. Of form df_name
                item - column name we want in list
    '''
    if item == "User_id":
        retrieved_list = df[item].to_list()
        for i in range(len(retrieved_list)):
            retrieved_list[i] = user_id_format(retrieved_list[i])
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
        user_id = user_id_format(row['User_id'].iloc[0])
    else:
        identifier = int(identifier)
        row = df[df['User_id']==identifier]
        username = row['Username'].iloc[0]
        user_id = user_id_format(identifier)

    firstname = row['Name'].iloc[0]
    surname = row['Surname'].iloc[0]
    password = row['Password'].iloc[0]

    customer = Customers.Customers(firstname, surname, username, user_id, password)

    return customer

# call_customer_from_db('jimmy')

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
    if db == 'customers':
        customers_dir = get_dbdirectory(db)
        df = get_dbasdf(db)
        customer_details = instance.get_detailslist()
        column_names = list(df)
        df_newcustomer = pd.DataFrame([customer_details], columns = column_names)
        df = pd.concat([df, df_newcustomer], ignore_index = False)
        df.to_csv(customers_dir, index = False)
    
    elif db == 'paymentcards':
        print('to-do')
        # if payment card exists, then update amount
        # else - i.e. doesn't exist - then add



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
    print('3 -- Back')
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
    print('4 -- View my gift-card/payment-card balances')
    print('5 -- Add gift-card or payment-card')
    print('6 -- Exit')
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
                prompt = user_id_format(prompt)
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

    
def check_date_valid(date):
    '''
    returns true or false depending on whether the date provided is valid (true) or not (false)
    '''
    day, month, year = date.split('/')
    try:
        datetime(int(year), int(month), int(day))
        return True
    except ValueError:
        return False

def check_paymentcard_valid(card_number):
    '''
    simply checking that does not already exist in db and that of correct form
    '''


# print(check_date_valid('09/14/22'))
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
        welcome_menu]
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
    max_id = 0
    for ids in user_ids:
        ids = int(ids)
        if ids > max_id:
            max_id = ids
    # temporarily string instead of integer in db, but causes no issues
    user_id = user_id_format(max_id + 1)
    
    customer = Customers.Customers(firstname, surname, username, user_id, password)
    
    modify_db(customer, 'customers')

    print_bars()
    print(f'Welcome, {username} !')
    print(customer)

    return customer


def new_paymentcard(customer):
    '''
    returns list of paymentcard instances
    '''
    # while card_number not 
    #     card_number = 
    # while expiry_date
    #     expiry_date = 
    # card_balance = 0
    # while type(card_balance) <= int:
    #     card_balance = 



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
        exit]
    }

    next_menu = option_menu(customer_menu_dic)

    if next_menu == 1:
        print('new order')
    elif next_menu == 2:
        print('orders in progress')
    elif next_menu == 3:
        print('order history')
    elif next_menu == 4:
        print('add gift card/payment card')
    elif next_menu == 5:
        print('view payment cards')
        

def display_paymentcards(customer):
    '''
    returns list of paymentcard instances
    '''
    print('')


def use_paymentcards(customer):
    '''
    returns list of paymentcard instances
    '''
    print('')

# customer = Customers.Customers('Alex', 'Tester', 'tester', '000000003', 'test')

def main():
    customer = welcome_menu()

    order = customer_menu(customer)

    exit()


# def last_menu(menu):
#     if menu == 'welcome':
#         print_bars()
#         print('Returning to Welcome Menu')
#         welcome_menu()
#     elif menu == 'signin':
#         print_bars()
#         print('Returning to Sign-in Menu')
#         signin_menu()
#     elif menu == 'signup':
#         print_bars()
#         print('Returning to Sign-up Menu')
#         signup_menu()
#     # elif payment:
#     elif menu == '':
#         print_bars()
#         print('Back to function called without adequate parameters set')
#         print_bars()    
#     elif menu == 'main':
#         main()


###################################################################################################    


main()