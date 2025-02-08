from django.urls import path
from complaint import views


urlpatterns = [
    path('', views.sample, name='sample'),
    path('user-complaint/<int:user_id>/', views.customer_complaints, name='customer_complaints'),
    path('complaint/update/<int:pk>/', views.update_complaint, name='update_complaint'),
    path('complaint/add/', views.add_complaint, name='add_complaint'),
    path('users/', views.user, name='users'),
    path('crete-user/', views.add_user, name='add_user'),
    path('user/update/<int:pk>/', views.update_user, name='update_user'),
]