from django.http import JsonResponse
#Json message when user submits an invalid parameter to the API
def error_404(request, exception):
    response = JsonResponse(data={"message": "Endpoint does not exist", "status_code": 404})
    response.status_code = 404
    return response