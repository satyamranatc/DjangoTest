from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hardcoded_test_view(request):
    data = {
        "message": "This is hardcoded data for testing DRF project setup!",
        "status": "success",
        "data": {
            "user": "Satyam Rana",
            "role": "Developer",
            "technologies": ["Django", "Django REST Framework", "Python"],
            "project": "DjangoTest"
        }
    }
    return Response(data)
