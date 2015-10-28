**********
Validators
**********

To run actions, the app must receive some sort of a trigger request, e.g. a push notification from GitHub. The app checks all incoming requests, and only the ones that pass the check trigger actions. The requests usually contain data that should be passed to the actions, i.e. branch name, so the app must extact the data after the check.

In Sloth  CI, a trigger request source is called *provider*; e.g., GitHub, Bitbucket, and GitLab are providers. Each provider uses its own request format and thus requires its own validation and data extraction routine.

**Validator** implements request checking and data extraction for a particular provider. To add support of a new provider to Sloth CI, we just create a corresponsing validator.

Here is the list of currently available validators. If you want to create your own validator, refer to the :doc:`developer guide <dev/validator>`.


.. _bitbucket-validator:

Bitbucket
=========

.. automodule:: sloth_ci.validators.bitbucket
    :members:


.. _github-validator:

GitHub
======

.. automodule:: sloth_ci.validators.github
    :members:


.. _gitlab-validator:

GitLab
======

.. automodule:: sloth_ci.validators.gitlab
    :members: