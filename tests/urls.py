# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from template_tree.urls import urlpatterns as django_template_tree_urls

app_name = 'template_tree'

urlpatterns = [
    url(r'^', include(django_template_tree_urls, namespace='django_template_tree')),
]
