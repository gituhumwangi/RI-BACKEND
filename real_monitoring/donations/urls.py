from django.urls import path
from . import views

urlpatterns = [
    # User URLs
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/new/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user-update'),

    # Donation URLs
    path('donations/', views.donation_list, name='donation-list'),
    path('donations/<int:pk>/', views.donation_detail, name='donation-detail'),
    path('donations/new/', views.donation_create, name='donation-create'),
    path('donations/<int:pk>/verify/', views.donation_verify, name='donation-verify'),

    # Message URLs
    path('messages/', views.message_list, name='message-list'),
    path('messages/new/', views.message_create, name='message-create'),

    # Business Profile URLs
    path('business_profiles/', views.BusinessProfileListView.as_view(), name='business-profile-list'),
    path('business_profiles/<int:pk>/', views.BusinessProfileDetailView.as_view(), name='business-profile-detail'),
    path('business_profiles/new/', views.BusinessProfileCreateView.as_view(), name='business-profile-create'),
    path('business_profiles/<int:pk>/edit/', views.BusinessProfileUpdateView.as_view(), name='business-profile-update'),
]
