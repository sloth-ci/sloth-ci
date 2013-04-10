configs: Configuration for Humans
==================================

Parsing INI-format configurations with the standard library configparser is painful.

**configs** provides an easy and clean API for configuration file parsing.

It supports values without section, automatically converts numeric values, automatically handles sections with listed values as lists.

Configurations are easy as they should be in Python!

Installation
------------

    pip install configs

Usage
-----

Sample config (``sample.conf``):

    top_level = value

    [general]
    spam = eggs
    foo: bar

    [list_section]
    1
    2.2
    3

    [mixed]
    prop = val
    flag

Usage:

    >>> import configs

    >>> conf = configs.load('sample.conf')

    >>> print(conf)                         #All config values
    {'general': {'foo': 'bar', 'spam': 'eggs'}, 'root': {'top_level': 'value'}, 'list_section': [1, 2.2, 3], 'mixed': (['flag'], {'prop': 'val'})}

    >>> print(conf['root'])                 #Top-level items are stored in the root section
    {'top_level': 'value'}

    >>> print(conf['general'])              #Values from the general section
    {'foo': 'bar', 'spam': 'eggs'}

    >>> print(conf['general']['foo'])       #Value of the foo parameter in the general section
    bar

    >>> for i in conf['list_section']:      #Sections are iterable
    ...     print(i * 2)                    #Numeric values are automatically converted to numbers
    ...
    2
    4.4
    6

    >>> for k in conf['general']:           #Key-value sections are also iterable
    ...     print(k)
    ...
    eggs
    bar

    >>> mixed_section = conf['mixed']
    >>> for m in mixed_section:             #Even mixed sections are iterable: listed values first, key-value next
    ...     print(m)
    ...
    flag
    val

    >>> print(mixed_section.dict_props)            #It is possible to get key-value items separetely...
    {'prop': 'val'}

    >>> print(mixed_section.list_props)            #...as well as list values
    ['flag']
