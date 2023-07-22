from django.urls import path

from .views import *

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('sign-in/', SignInView.as_view()),
    path('document/', DocumentView.as_view()),
    path('document/<int:pk>/', DocumentDetailView.as_view()),
]

