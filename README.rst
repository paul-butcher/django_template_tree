=============================
django-template_tree
=============================

.. image:: https://badge.fury.io/py/django_template_tree.svg
    :target: https://badge.fury.io/py/django_template_tree

.. image:: https://travis-ci.org/paul-butcher/django_template_tree.svg?branch=master
    :target: https://travis-ci.org/paul-butcher/django_template_tree

.. image:: https://codecov.io/gh/paul-butcher/django_template_tree/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/paul-butcher/django_template_tree

Generate diagrams showing relationships between templates in Django projects

Documentation
-------------

The full documentation is at https://django_template_tree.readthedocs.io.

Quickstart
----------

Install django-template_tree::

    pip install django_template_tree

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'template_tree',
        ...
    )

Add django-template_tree's URL patterns:

.. code-block:: python

    from template_tree import urls as template_tree_urls
    from django import settings
    if settings.DEBUG:
        urlpatterns += [
            url(r'^__tt__/', include('template_tree.urls', namespace='template_tree')),
        ]

Features
--------

Displays a collapsible tree diagram showing the hierarchy of templates used by a Django application.

.. image:: _static/screenshot.png

Nodes can be collapsed and expanded, by clicking on them.

.. image:: _static/screenshot-collapsed.png

Apps can be filtered out of the tree, using the 'exclude_app' querystring parameter, thus:

http://localhost:8000/__tt__/?exclude_app=template_tree&exclude_app=admin

By default, admin is excluded, so
http://localhost:8000/__tt__/
is equivalent to
http://localhost:8000/__tt__/?exclude_app=admin

In order to show the admin app as well, you will need to 'unexclude' it thus:
http://localhost:8000/__tt__/?exclude_app=

Visiting the template_tree url, requesting an application/json response will return json data
compatible with d3 hierarchies, so you can roll your own diagrams.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
