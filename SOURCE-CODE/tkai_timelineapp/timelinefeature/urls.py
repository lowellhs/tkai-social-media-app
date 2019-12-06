from django.urls import path
from .views import create, delete, update, find
#url for app
urlpatterns = [
    path('create/', create, name="create"),
    path('delete/', delete, name="delete"),
    path('update/', update, name="update"),
    path('find/', find, name="find"),
]
