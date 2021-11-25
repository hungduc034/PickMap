from django.urls import path
from products import views

urlpatterns = [
    path('products/', views.snippet_list),
    path('products/<int:pk>/', views.snippet_detail),
]