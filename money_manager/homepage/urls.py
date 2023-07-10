from django.urls import path
from . import views

urlpatterns= [
    path('<str:pk>/', views.homepage, name='homepage'),
    path('transaction/<str:pk>/', views.transaction, name='transaction'),
]