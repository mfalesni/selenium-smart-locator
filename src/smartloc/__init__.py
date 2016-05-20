# -*- coding: utf-8 -*-
import re
import six
from collections import namedtuple
from selenium.webdriver.common.by import By

__all__ = ['Locator']
__version__ = '0.1.1'


class Locator(namedtuple('Locator', ['by', 'locator'])):
    """Class encapsulating generating of the Selenium locators.

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
    :py:class:`Locator` to parse the entries. Or anything else.

    Available selector strategies:

    * class_name
    * css
    * id
    * link_text
    * name
    * partial_link_text
    * tag
    * xpath

    """
    CLASS_SELECTOR = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9]*)?(?:[#.][a-zA-Z0-9_-]+)+$")
    BY_MAPPING = {
        'class_name': By.CLASS_NAME,
        'css': By.CSS_SELECTOR,
        'id': By.ID,
        'link_text': By.LINK_TEXT,
        'name': By.NAME,
        'partial_link_text': By.PARTIAL_LINK_TEXT,
        'tag': By.TAG_NAME,
        'xpath': By.XPATH,
    }

    @classmethod
    def by_class_name(cls, locator):
        return cls(By.CLASS_NAME, locator)

    @classmethod
    def by_css(cls, locator):
        return cls(By.CSS_SELECTOR, locator)

    @classmethod
    def by_id(cls, locator):
        return cls(By.ID, locator)

    @classmethod
    def by_link_text(cls, locator):
        return cls(By.LINK_TEXT, locator)

    @classmethod
    def by_name(cls, locator):
        return cls(By.NAME, locator)

    @classmethod
    def by_partial_link_text(cls, locator):
        return cls(By.PARTIAL_LINK_TEXT, locator)

    @classmethod
    def by_tag(cls, locator):
        return cls(By.TAG_NAME, locator)

    @classmethod
    def by_xpath(cls, locator):
        return cls(By.XPATH, locator)

    def __new__(cls, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], cls):
                # If it is a Locator already, return it straight away
                return args[0]
            elif isinstance(args[0], dict):
                # Process dict as kwargs
                return cls(**args[0])
            elif isinstance(args[0], six.string_types):
                # Determine whether it is a simple css selector or an xpath
                css = cls.CLASS_SELECTOR.match(args[0])
                if css is not None:
                    by = By.CSS_SELECTOR
                    locator = css.group()
                else:
                    by = By.XPATH
                    locator = args[0]
            elif hasattr(args[0], '__locator__'):
                # __locate__ protocol
                return cls(args[0].__locator__())
            else:
                raise TypeError('Cannot parse {0} into a valid locator!'.format(repr(args[0])))
        elif len(args) == 2:
            # Mimic an ordinary 2-tuple
            by, locator = args
            if not By.is_valid(by):
                raise ValueError('{0} is not a recognized resolution strategy'.format(by))
        elif len(args) == 0 and kwargs:
            by = None
            locator = None
            for k, v in kwargs.items():
                if k == 'by':
                    if v not in cls.BY_MAPPING:
                        raise ValueError('{0} is not a recognized resolution strategy'.format(v))
                    by = cls.BY_MAPPING[v]
                elif k == 'locator':
                    locator = v
                elif k in cls.BY_MAPPING:
                    by = cls.BY_MAPPING[k]
                    locator = v
                else:
                    raise ValueError('Unrecognized parameter {0} for Locator'.format(k))
            if by is None:
                raise ValueError('by was not specified')
            if locator is None:
                raise ValueError('locator was not specified')
        else:
            raise TypeError('Wrong parameters specified for locator. See Locator class docstring.')
        return super(Locator, cls).__new__(cls, by, locator)

    # Convenience methods
    def find_element(self, browser_or_element):
        """A convenience method for interacting with Selenium. Calls Selenium's find_element()

        Args:
            browser_or_element: Browser or Element objects where to query from.

        Returns:
            A Selenium WebElement.
        """
        return browser_or_element.find_element(*self)

    def find_elements(self, browser_or_element):
        """A convenience method for interacting with Selenium. Calls Selenium's find_elements()

        Args:
            browser_or_element: Browser or Element objects where to query from.

        Returns:
            A list of Selenium WebElement objects.
        """
        return browser_or_element.find_elements(*self)
