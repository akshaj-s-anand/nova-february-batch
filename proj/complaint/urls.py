from django.urls import path
from complaint import views


urlpatterns = [
    path('', views.complaint_list, name='complaint_list'),
    path('user-complaint/<int:user_id>/', views.complaint_list, name='customer_complaints'),
    path('complaint/update/<int:pk>/', views.update_complaint, name='update_complaint'),
    path('complaint/add/', views.add_complaint, name='add_complaint'),
    path('users/', views.user_list, name='users'),
    path('crete-user/', views.add_user, name='add_user'),
    path('user/update/<int:pk>/', views.update_user, name='update_user'),
]