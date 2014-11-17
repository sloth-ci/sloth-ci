**********
Validators
**********

Each validator corresponds to a different type of incoming payload, or *provider*. Every :doc:`app <apps>` must specify its provider, therefore use a certain validator to check the payload.

A validator excepts a ChettyPy request object and can check it in any way you like. For example, the ``bitbucket`` validator checks the request's method (must be POST), origin (must come from a trusted IP), and the repository name.

Whereas some data can be obtained directly from the request (like IP and method), some data must be specified by the user, e.g. the repository they are interested in.

Apart from validating the payload, a validator can extract valuable data from it. The ``bitbucket`` validator extracts the branch name, so you can refer to it your actions.

Validators are installed from PyPI with ``pip install sloth-ci.validators.<validator>``.

Sloth CI validators live in a separate repository a https://bitbucket.org/moigagoo/sloth-ci-validators/.

When writing your own validators, refer to the :ref:`dummy validator <dummy-validator>`.

Bitbucket
=========

.. automodule:: sloth_ci.validators.bitbucket

.. _dummy-validator:

Dummy
=====

.. automodule:: sloth_ci.validators.dummy

GitHub
======

.. automodule:: sloth_ci.validators.github