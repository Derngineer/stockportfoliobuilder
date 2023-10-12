from django.urls import path, include
from . import app_dash
from . import views


urlpatterns = [
     path('', views.login_view, name='login'),
    path("settings/", views.settings, name="settings"),
    path("portfolio_builder/", views.portfolio_building, name ="building"),
    path("portfolio_tester/", views.portfolio_testing, name="testing"),
    path('register/', views.register, name='register'),   
    path('logout/', views.user_logout, name='logout'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]

