from rest_framework import renderers
import json

class CustomStatusRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'ErrorDetail' in str(data):
            # Convert errors to the desired format
            formatted_errors = {'errors': {'details': [str(detail) for detail in data]}}
            response = json.dumps(formatted_errors)
        else:
            response = json.dumps(data)
        return response