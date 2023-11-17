from django.urls import path

from .views import FormAPI, CreateFormAPI

urlpatterns = [
    path('get_form/', FormAPI.as_view()),
    path('create_form/', CreateFormAPI.as_view()),
]
