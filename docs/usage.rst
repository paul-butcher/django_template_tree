=====
Usage
=====

To use django-template_tree in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_template_tree.apps.DjangotemplateTreeConfig',
        ...
    )

Add django-template_tree's URL patterns:

.. code-block:: python

    from django_template_tree import urls as django_template_tree_urls


    urlpatterns = [
        ...
        url(r'^', include(django_template_tree_urls)),
        ...
    ]
