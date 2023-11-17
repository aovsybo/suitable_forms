from django.urls import path

from .views import FormAPI, CreateFormAPI

urlpatterns = [
    path('get_form/', FormAPI.as_view(), name='get-form'),
    path('create_form/', CreateFormAPI.as_view(), name='create-form'),
]
