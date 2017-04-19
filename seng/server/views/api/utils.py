import json

from collections import OrderedDict
from django.http import HttpResponseBadRequest

def err(message):
    return HttpResponseBadRequest(get_error_json(message), content_type='application/json')

def get_error_json(message):
    return json.dumps(OrderedDict([
            ('error', message),
            ('success', False)
        ]))