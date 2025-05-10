from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/register/', views.UserRegisterViews.as_view(), name='user-register'),
    path('auth/login/', views.UserLoginView.as_view(), name='user-login'),
    path('auth/verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='user-logout'),

]
