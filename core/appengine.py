'''app engine'''
from shoppinglistapp.core.items import Item


class AppEngine:
    '''app engine class'''
    def __init__(self, shopping_list_arg=None, items=None):
        self.items = items
        self.shopping_list = shopping_list_arg
        self.continue_execution = True
        self.message = None
        self.correct_answer = None
        self.status = None

    def process_answer(self, cmd):
        '''process answer'''
        if (isinstance(cmd, float)) or (cmd.replace(".", "").isnumeric()):
            # validate cmd string has only numbers
            answer = round(float(cmd), 2)
            if answer == self.correct_answer:
                self.message = 'Correct!'
            else:
                self.message = '' # f'Not Correct! (Expected \
                    # ${self.correct_answer:.02f})\nYou answered \
                    # ${answer:.02f}.'
        else:
            self.message = 'The provided answer is not a valid number!'
        self.correct_answer = None  # is it in right place?

    def process_add_item(self, cmd):
        '''process add item'''
        item_str = cmd[4:]
        item_tuple = item_str.split(': ')
        if len(item_tuple) == 2:
            name, price = item_tuple
            if price.replace(".", "").isnumeric():
                # validate price str has only numbers
                price = float(price)
                if name != '':  # validate name is not empty
                    item = Item(name, price)
                    if item.name in self.items.items:
                        # validate item added is not duplicate
                        self.message = 'Duplicate!'
                    else:
                        self.items.add_item(item)
                        self.message = f'{item} added successfully.'
                else:
                    self.message = 'Item name string cannot be empty.'
            else:
                if '-' in price:
                    price = price.strip('-')
                    self.message = f'The price argument \
                        ("-{float(price)}") does not appear to \
                        be any of the following: float, an integer, \
                        or a string that can be parsed to a \
                        non-negative float'
                else:
                    self.message = f"could not convert string \
                        to float: '{price}'"
        else:
            self.message = f'Cannot add "{item_str}".\n'
            self.message += 'Usage: add <item_name>: <item_price>'

    def process_del_item(self, cmd):
        '''process del item'''
        item_name = cmd[4:]
        if item_name in self.items.items: 
            self.items.remove_item(item_name)
            self.message = f'{item_name} removed successfully.'
        else:
            self.message = f'Item named "{item_name}" is not present in the item pool.'
