from django.urls import path
from . import views

urlpatterns = [
    path('mock-upgrade/', views.mock_upgrade_view, name='mock_upgrade'),
]
