from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [
    path('token/create_token/',LoginView.as_view()),
    path('token/refresh_token/',TokenRefreshView.as_view()),
    path('get_shablon_data/',get_shablon_data),
    path('change_shablon_data/',change_shablon_data),

]