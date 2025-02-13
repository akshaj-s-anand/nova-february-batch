from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('permission-denied/', views.permission_denied, name='permission_denied'),
    path('view-item/', views.viewwitem, name='view_item'),
    path('add-item/', views.add_or_update_item, name='add_item'),
    path('item/update/<int:pk>/', views.add_or_update_item, name='update_item'),
    path('complaint-statuses/', views.view_complaint_statuses, name='view_complaint_statuses'),
    path('complaint-statuses/add/', views.add_or_update_complaint_status, name='add_complaint_status'),
    path('complaint-statuses/edit/<int:pk>/', views.add_or_update_complaint_status, name='edit_complaint_status'),
]   