import json

from django.http import HttpResponse
from django.shortcuts import render

from . import template_reader


def default_view(request):

    if 'html' in request.META['HTTP_ACCEPT']:
        return render(request, "template_tree/tree.html")
    elif 'application/json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(
            json.dumps(template_reader.all_templates(request.GET.get('exclude_app',None))),
            content_type='application/json'
        )
