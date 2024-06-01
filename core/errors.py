'''py file with error classes'''


class InvalidItemNameError(Exception):
    '''invalid name error class'''
    def __init__(self, item):
        if not isinstance(item, str):
            super().__init__(f'Item name must be a string (not {type(item)}).')
        else:
            super().__init__('Item name string cannot be empty.')


class InvalidItemPriceError(Exception):
    '''invalid item price class'''
    def __init__(self, price):
        super().__init__(f'The price argument ("{price}") \
                        does not appear to be any of the \
                        following: float, an integer, or \
                        a string that can be parsed to a non-negative float.')


class InvalidItemPoolError(Exception):
    '''invalid item pool class'''
    def __init__(self):
        super().__init__('ItemsPool needs to be set as \
                         a dictionary with non-empty strings \
                         as keys and Item instances as values.')


class NonExistingItemError(Exception):
    '''non existing item error class'''
    def __init__(self, item_name):
        super().__init__(f'Item named "{item_name}" is not \
                         present in the item pool.')


class DuplicateItemError(Exception):
    '''duplicate item error class'''
    def __init__(self):
        super().__init__('Duplicate!')


class InvalidShoppingListSizeError(Exception):
    '''invalid shopping list size class'''
    def __init__(self):
        super().__init__('Invalid List Size!')
