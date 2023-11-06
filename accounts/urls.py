from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.Login_api_view),
    path('Signaup', views.Siginup_api_view)
]