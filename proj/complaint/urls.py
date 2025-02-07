from django.urls import path
from . import views

urlpatterns = [
    path('', views.sample, name='sample'),
    path('complaints/<int:user_id>/', views.customer_complaints, name='customer_complaints'),
]