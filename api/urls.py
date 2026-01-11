from django.urls import path
from .views import hardcoded_test_view

urlpatterns = [
    path('test-data/', hardcoded_test_view, name='test_data'),
]
