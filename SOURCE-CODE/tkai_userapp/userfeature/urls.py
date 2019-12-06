from django.urls import path
from .views import login, regis, get_detail_user, update_profile
#url for app
urlpatterns = [
    path('login/', login, name="login"),
    path('regis/', regis, name="regis"),
    path('detail/', get_detail_user, name="detail"),
    path('update/', update_profile, name="update"),
]
