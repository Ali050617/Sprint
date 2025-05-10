from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterViews.as_view(), name='register'),

]