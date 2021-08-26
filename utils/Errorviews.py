from django.http import JsonResponse
def error_404(request, exception):
    print(exception)
    print(request)
    response = JsonResponse(data={"message": "Endpoint does not exist", "status_code": 404})
    response.status_code = 404
    return response