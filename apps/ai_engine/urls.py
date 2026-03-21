from django.urls import path
from . import views

urlpatterns = [
    path("generate/", views.generate_captions_view, name="generate_captions"),
    path("history/", views.history_view, name="history"),
]