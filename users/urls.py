from django.urls import path
from .views import register_view, login_view, logout_view, profile_view, seller_dashboard

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('seller_dashboard/', seller_dashboard, name='seller_dashboard'),
]