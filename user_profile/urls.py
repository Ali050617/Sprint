from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/register/', views.UserRegisterViews.as_view(), name='user-register'),
    path('auth/login/', views.UserLoginView.as_view(), name='user-login'),
    path('auth/verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('auth/password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('auth/password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    path('users/me/', views.UserDataView.as_view(), name='user'),

    path('profiles/<str:username>/', views.UserProfileView.as_view(), name='user-profile'),


]
