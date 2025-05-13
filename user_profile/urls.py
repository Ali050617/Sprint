from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('auth/register/', views.UserRegisterViews.as_view(), name='user-register'),
    path('auth/login/', views.UserLoginView.as_view(), name='user-login'),
    # path('auth/verify-email/', views.EmailVerificationView.as_view(), name='verify-email'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('auth/password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('auth/password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    path('users/me/', views.UserDataView.as_view(), name='user-data'),

    path('profiles/me/', views.UserRetrieveUpdateView.as_view(), name='user-profile-update'),
    path('profiles/<str:username>/', views.UserProfileView.as_view(), name='user-profile-view'),

    path('profiles/<str:username>/follow/', views.FollowUserView.as_view(), name='user-follow'),
    path('profiles/<str:username>/unfollow/', views.UnfollowUserView.as_view(), name='user-unfollow'),
    path('profiles/<str:username>/followers/', views.FollowersListView.as_view(), name='user-followers'),
    path('profiles/<str:username>/following/', views.FollowingListView.as_view(), name='user-following'),
]
