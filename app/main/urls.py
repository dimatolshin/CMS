from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenBlacklistView


urlpatterns = [
    path('token/create_token/',LoginView.as_view()),
    path('token/refresh_token/',TokenRefreshView.as_view()),
    path('token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('test_point/',test_point),
    path('get_shablon_data/',get_shablon_data),
    path('change_shablon_data/',change_shablon_data),
    path('take_bot_data/',take_bot_data),
    path('get_all_domain/',get_all_domain),
    path('get_all_server/',get_all_server)


]