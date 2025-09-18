import pytest
from Func_1 import add_product, login, register, sellers, products

def test_add_product():
    assert add_product(1, "Product A", 100, 10) == 0
    assert add_product(1, "", 100, 10) == 5
    assert add_product(1, "Product A", -100, 10) == 4
    assert add_product(1, "Product A", 100, -10) == 6
    assert add_product(1, "Product A", 100, 0) == 6
    
def test_register():
    assert register()