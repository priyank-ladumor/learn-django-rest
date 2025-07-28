from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

class CustomJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response', None)

        # Handle errors: don't wrap DRF errors
        if response is not None and not str(response.status_code).startswith('2'):
            # Format message from common error formats
            if isinstance(data, dict):
                if 'detail' in data:
                    message = data['detail']
                else:
                    # Construct a message from field errors
                    messages = []
                    for field, errors in data.items():
                        if isinstance(errors, list):
                            messages.append(f"{field} - {', '.join(errors)}")
                        else:
                            messages.append(f"{field} - {str(errors)}")
                    message = "Validation failed: " + "; ".join(messages) if messages else "error"
            elif isinstance(data, list) and data:
                message = str(data[0])
            else:
                message = "error"

            return super().render({
                'status': response.status_code,
                'message': message,
                'errors': data
            }, accepted_media_type, renderer_context)

        # Successful response formatting
        formatted = {
            'status': response.status_code if response else 200,
            'isSuccess': True,
            'message': 'success',
            'data': data if isinstance(data, (dict, list, ReturnDict, ReturnList)) else {}, # isinstance(data, (dict, list)) checks if data is a dictionary or list
        }

        return super().render(formatted, accepted_media_type, renderer_context)
