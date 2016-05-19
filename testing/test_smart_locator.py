# -*- coding: utf-8 -*-
import pytest
from mock import Mock
from selenium.webdriver.common.by import By

from smartloc import Locator


def test_selenium_like():
    assert Locator(By.XPATH, '//h1') == (By.XPATH, '//h1')


def test_nested_locator():
    loc = Locator(By.XPATH, '//h1')
    loc2 = Locator(loc)
    assert loc2 == (By.XPATH, '//h1')
    assert loc2 is loc


def test_no_params():
    with pytest.raises(TypeError):
        Locator()


def test_bad_param():
    with pytest.raises(TypeError):
        Locator(1)


def test_many_params():
    with pytest.raises(TypeError):
        Locator('foo', 'bar', 'baz')


def test_bad_strategy_tuple():
    with pytest.raises(ValueError):
        Locator('foo', 'bar')


def test_bad_strategy_kwarg():
    with pytest.raises(ValueError):
        Locator(by='foo', locator='bar')


def test_bad_kwarg():
    with pytest.raises(ValueError):
        Locator(foo='bar')


def test_kwargs_no_by():
    with pytest.raises(ValueError):
        Locator(locator='bar')


def test_kwargs_no_locator():
    with pytest.raises(ValueError):
        Locator(by='xpath')


def test_simple_css():
    assert Locator('foo#bar.baz.bat') == (By.CSS_SELECTOR, 'foo#bar.baz.bat')
    assert Locator('#bar.baz.bat') == (By.CSS_SELECTOR, '#bar.baz.bat')
    assert Locator('#bar') == (By.CSS_SELECTOR, '#bar')
    assert Locator('.bat') == (By.CSS_SELECTOR, '.bat')


def test_implicit_xpath():
    assert Locator('//h1') == (By.XPATH, '//h1')


def test_locator_protocol_and_dict_kwargs():
    class Class(object):
        def __init__(self, loc):
            self.loc = loc

        def __locator__(self):
            return self.loc

    assert Locator(Class('#foo')) == (By.CSS_SELECTOR, '#foo')
    assert Locator(Class({'xpath': '//h1'})) == (By.XPATH, '//h1')


def test_locator_find_element():
    selenium = Mock(spec=['find_element'])
    locator = Locator(xpath='//h1')

    locator.find_element(selenium)

    selenium.find_element.assert_called_once_with(By.XPATH, '//h1')


def test_locator_find_elements():
    selenium = Mock(spec=['find_elements'])
    locator = Locator(xpath='//h1')

    locator.find_elements(selenium)

    selenium.find_elements.assert_called_once_with(By.XPATH, '//h1')
