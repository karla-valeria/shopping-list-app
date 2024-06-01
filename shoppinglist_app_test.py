import math
import pytest
from shoppinglistapp.core.items import Item, ItemPool
from shoppinglistapp.core.appengine import AppEngine
from shoppinglistapp.core.shoppinglist import ShoppingList
from shoppinglistapp.core.errors import InvalidItemNameError, InvalidItemPriceError, InvalidItemPoolError, DuplicateItemError, NonExistingItemError, InvalidShoppingListSizeError
from shoppinglistapp.app_cli import AppCLI

'''test items.py'''
# test item class
def test_valid_item_init():
    item = Item('bread', 3.25)
    assert item.name == 'bread'
    assert math.isclose(item.price, 3.25)

def test_invalid_item_init():
    with pytest.raises(InvalidItemNameError):
        Item('', 3.25)
    with pytest.raises(InvalidItemNameError):
        Item(True, .99)
    with pytest.raises(InvalidItemPriceError):
        Item('bread', -3.25)

def test_item_get_order():
    item = Item('bread', 3.25)
    assert item.get_order() == 0
    item.price = 1000.0
    assert item.get_order() == 3

def test_item_get_list_item_str():
    item = Item('bread', 3.25)
    assert item.get_list_item_str(quantity=2) == '- bread (2x)'
    assert item.get_list_item_str(
        quantity=2, leading_dash=True) == '- bread (2x)'
    assert item.get_list_item_str(leading_dash=True) == '- bread'
    
def test_item_get_price_str():
    item = Item('bread', 3.25)
    assert item.get_price_str() == '$3.25'
    assert item.get_price_str(hide_price=True) == '$?.??'
    assert item.get_price_str(order=3) == '$0003.25'
    
    
def test_item_repr():
    item = Item('bread', 3.25)
    assert repr(item) == 'Item(bread, 3.25)'
    
def test_item_eq():
    item1 = Item('bread', 3.25)
    item2 = Item('bread', 3.25)
    item3 = Item('butter', 4.10)
    assert item1 == item2
    assert item1 != item3

#test ItemPool class
def test_valid_item_pool_init():
    item_pool = ItemPool()
    assert item_pool.items == {}

def test_invalid_item_pool_init():
    with pytest.raises(InvalidItemPoolError):
        ItemPool(('bread', 1.00))
    with pytest.raises(InvalidItemPoolError):
        item1 = Item('bread', 1.00)
        ItemPool({1: item1})

def test_add_item():
    with pytest.raises(InvalidItemPoolError):
        item = 'hi'
        item_pool = ItemPool({})
        item_pool.add_item(item)
    with pytest.raises(DuplicateItemError):
        item_pool = ItemPool()
        item = Item('banana', 0.99)
        item_pool.add_item(item)
        item_pool.add_item(item)

def test_remove_item():
    with pytest.raises(NonExistingItemError):
        item_pool = ItemPool()
        item = Item('banana', 0.99)
        item_pool.add_item(item)
        item_pool.remove_item('banana')
        item_pool.remove_item('banana')

def test_get_size():
    item_pool = ItemPool({})
    assert item_pool.get_size() == 0

def test_sample_items():
    item1 = Item('banana', 1.00)
    item2 = Item('shoes', 20.00)
    item_pool = ItemPool({'banana': item1, 'shoes': item2})
    assert item_pool.sample_items(1) == [item1] or [item2]

def test_item_pool_repr():
    item = Item('bread', 0.99)
    item_pool = ItemPool()
    item_pool.add_item(item)
    assert repr(item_pool) == f'ItemPool({item_pool.items})'

def test_item_pool_eq():
    ip_1 = ItemPool({'bread': Item('bread', 0.99)})
    ip_2 = ItemPool({'bread': Item('bread', 0.99)})
    ip_3 = ItemPool()
    assert ip_1 == ip_2
    assert ip_1 != ip_3


'''test shoppinglist.py'''
def test_shoppinglist_init():
    sp = ShoppingList()
    assert sp.list == []

def test_shoppinglist_refresh():
    item2 = Item('Macbook', 1999.99)
    item3 = Item('Milk', 4.25)
    ip = ItemPool()
    ip.add_item(item2)
    ip.add_item(item3)
    sp = ShoppingList()
    sp.refresh(ip)
    assert len(sp.list) > 0
    with pytest.raises(ValueError):
        sp.refresh(ip, size='hi')
    with pytest.raises(ValueError):
        sp.refresh(ip, quantities=3)
    with pytest.raises(ValueError):
        sp.refresh(ip, quantities=[3, 'hi'])
    with pytest.raises(InvalidShoppingListSizeError):
        sp.refresh(ip, size=3)
    sp.refresh(ip, size=2, quantities=[2])
    assert sp.list[1] == (Item('Milk', 4.25), 1) or (Item('Macbook', 1999.99), 1)
    sp.refresh(ip, size=1, quantities=[2, 2, 3])
    assert sp.list == [(Item('Macbook', 1999.99), 2)] or [(Item('Milk', 4.25), 2)]
    
def test_shoppinglist_get_total_price():
    item2 = Item('Macbook', 1999.99)
    ip = ItemPool()
    ip.add_item(item2)
    sp = ShoppingList(quantities=[1], item_pool=ip)
    assert sp.get_total_price() == 1999.99    

def test_shoppinglist_get_item_price():
    item2 = Item('Macbook', 1999.99)
    ip = ItemPool()
    ip.add_item(item2)
    sp = ShoppingList(quantities=[1], item_pool=ip)
    assert sp.get_item_price(0) == 1999.99  

def test_shoppinglist_len():
    item2 = Item('Macbook', 1999.99)
    item3 = Item('Milk', 4.25)
    ip = ItemPool()
    ip.add_item(item2)
    ip.add_item(item3)
    sp = ShoppingList(size=2, quantities=[1, 1], item_pool=ip)
    assert sp.__len__ != len(sp.list)


'''test appengine.py'''
def test_appengine_init():
    item2 = Item('Macbook', 1999.99)
    item3 = Item('Milk', 4.25)
    item4 = Item('Hotel Room', 255.00)
    item5 = Item('Beef Steak', 25.18)
    ip = ItemPool()
    ip.add_item(item2)
    ip.add_item(item3)
    ip.add_item(item4)
    ip.add_item(item5)
    sp = ShoppingList(size=3, quantities=[3, 2, 4], item_pool=ip)
    app_engine = AppEngine(sp, ip)
    assert app_engine.items == ip
    assert app_engine.shopping_list == sp

def test_appengine_process_answer():
    item2 = Item('Macbook', 1999.99)
    ip = ItemPool()
    ip.add_item(item2)
    sp = ShoppingList(size=1, quantities=[1], item_pool=ip)
    app = AppCLI(sp, ip)
    app.app_engine.process_answer('hi')
    assert app.app_engine.message == 'The provided answer is not a valid number!'
    app.process_ask()
    app.app_engine.process_answer(1999.99)
    assert app.app_engine.message == 'Correct!'
    app.app_engine.process_answer(100.00)
    assert app.app_engine.message != 'Correct!'

def test_process_add_item():
    item = Item('Macbook', 1999.99)
    ip = ItemPool()
    ip.add_item(item)
    sp = ShoppingList(size=1, quantities=[1], item_pool=ip)
    app = AppCLI(sp, ip)
    app.app_engine.process_add_item('    banana: 0.99')
    assert app.app_engine.message == 'Item(banana, 0.99) added successfully.'
    app.app_engine.process_add_item('    banana: 0.99')
    assert app.app_engine.message == 'Duplicate!'
    app.app_engine.process_add_item('    : 0.99')
    assert app.app_engine.message == 'Item name string cannot be empty.'
    app.app_engine.process_add_item('    banana: -0.99')
    assert app.app_engine.message == 'The price argument \
                        ("-0.99") does not appear to \
                        be any of the following: float, an integer, \
                        or a string that can be parsed to a \
                        non-negative float'
    app.app_engine.process_add_item('    banana: hi')
    assert app.app_engine.message == "could not convert string \
                        to float: 'hi'"
    app.app_engine.process_add_item('    banana: 0.99: hi')
    assert app.app_engine.message == 'Cannot add "banana: 0.99: hi".\nUsage: add <item_name>: <item_price>'

def test_process_del_item():
    item = Item('Macbook', 1999.99)
    ip = ItemPool()
    ip.add_item(item)
    sp = ShoppingList(size=1, quantities=[1], item_pool=ip)
    app = AppCLI(sp, ip)
    app.app_engine.process_del_item('del banana')
    assert app.app_engine.message == 'Item named "banana" is not present in the item pool.'
    app.app_engine.process_del_item('del Macbook')
    assert app.app_engine.message == "Macbook removed successfully."