import json

from collections import OrderedDict
from django.http import HttpResponse

def err(message):
    return HttpResponse(get_error_json(message), content_type='application/json')

def get_error_json(message):
    return json.dumps(OrderedDict([
            ('error', message),
            ('success', False)
        ]))