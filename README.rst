selenium-smart-locator
======================

|Build Status| |Coverage Status| |Code Health|

Class encapsulating generating of the Selenium locators.

It is designed to be simple and intuitive to use. It provides you various ways how to generate a
Selenium-compatible locators. The class is usable in Selenium element queries.

.. code-block:: python

    loc = Locator(By.XPATH, '//foo/bar/baz')    # Old selenium way of doing it
    element = s.find_element(*loc)              # Expand the tuple. That's how to use the class.

This is a basic sample of how does it work. Now come the usage samples of simplified locators:

.. code-block:: python

    # When you use this simple format of CSS consisting of tag name, ids and classes, it gets
    # detected automatically and the result is a CSS selector. IDs and classes are optional.
    Locator('div#foo.bar.baz')  # => Locator(by='css selector', locator='div#foo.bar.baz')
    # When you specify a plain string and it does not get matched be the preceeding CSS detector
    # it is assumed it is an XPath expression
    Locator('//h1') # => Locator(by='xpath', locator='//h1')
    # If you pass a Locator instance, it just goes straight through
    Locator(Locator('//h1')) # => Locator(by='xpath', locator='//h1')
    # If you have your own object, that implements __locator__(), then it can also be resolved
    # by the class. The __locator__() must either return Locator instance or
    # anything that Locator can process.
    Locator(my_obj)
    # You can leverage kwargs to say strategy=locator
    Locator(xpath='//h1')   # => Locator(by='xpath', locator='//h1')
    Locator(css='#something')   # => Locator(by='css selector', locator='#something')
    Locator(by='xpath', locator='//h1')   # => Locator(by='xpath', locator='//h1')
    # For your comfort, you can pass a dictionary, like it was kwargs
    Locator({'by': 'xpath', 'locator': '//h1'})   # => Locator(by='xpath', locator='//h1')
    # You can also use Locator's classmethods, like this:
    Locator.by_css('#foo')   # => Locator(by='css selector', locator='#foo')
    # Always in format Locator.by_<strategy_name>

When you have locators, you can avoid using ``*`` by using convenience methods:

.. code-block:: python

    l = Locator('#foo')
    browser = Firefox()
    element = l.find_element(browser)
    elements = l.find_elements(browser)

As you can see, the number of ways how to specify the input parameters offer you a great freedom
on how do you want to structure your locators. You can store them in YAML and you can use
Locator to parse the entries. Or anything else.

Available selector strategies:

* class_name
* css
* id
* link_text
* name
* partial_link_text
* tag
* xpath


License
=======

Licensed under GPLv3

.. |Build Status| image:: https://travis-ci.org/mfalesni/selenium-smart-locator.svg
   :target: https://travis-ci.org/mfalesni/selenium-smart-locator
.. |Coverage Status| image:: https://coveralls.io/repos/mfalesni/selenium-smart-locator/badge.svg
   :target: https://coveralls.io/r/mfalesni/selenium-smart-locator
.. |Code Health| image:: https://landscape.io/github/mfalesni/selenium-smart-locator/master/landscape.svg?style=flat
   :target: https://landscape.io/github/mfalesni/selenium-smart-locator/master
   :alt: Code Health
