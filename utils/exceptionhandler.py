from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    print("exc:", exc)
    print("context:", context)
    #get the defaukt exception handler
    response= exception_handler(exc, context)
    return response