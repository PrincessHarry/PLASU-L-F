from django.urls import path
from . import views
from .auth import logout_view

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('report-item/', views.report_item, name='report_item'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/<int:pk>/edit/', views.edit_item, name='edit_item'),
    path('lost-items/', views.lost_items, name='lost_items'),
    path('found-items/', views.found_items, name='found_items'),
    path('search/', views.search_items, name='search_items'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_read, name='mark_read'),
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('item/<int:item_id>/submit-claim/', views.submit_claim, name='submit_claim'),
    path('claim/<int:claim_id>/update-status/', views.update_claim_status, name='update_claim_status'),
    path('logout/', logout_view, name='logout'),
] 