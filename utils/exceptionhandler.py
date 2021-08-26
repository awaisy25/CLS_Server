from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    #get the defaukt exception handler
    response= exception_handler(exc, context)
    #handling loan total error from serilaizer
    if "Loan Total Error" in response.data[0]:
        print("Serializer Error handled by Custom Exception Handler")
        serializer_message = response.data[0].split("'")
        serializer_message = serializer_message[3]
        print(serializer_message)
        response.data = {"message": serializer_message}
        return response
    #print(response.__dict__)
    return response