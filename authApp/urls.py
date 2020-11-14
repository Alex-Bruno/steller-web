from django.urls import path
from .views import (
    GroupListView,
    GroupCreateView,
    GroupUpdateView,
    GroupDeleteView,
    #
    UserListView,
    export_users,
    print_users,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    UserChangePassword,
)

urlpatterns = [
    path('group/', GroupListView.as_view(), name='group_index'),
    path('group/new', GroupCreateView.as_view(), name='group_new'),
    path('group/<int:pk>/edit', GroupUpdateView.as_view(), name='group_edit'),
    path('group/<int:pk>/delete', GroupDeleteView.as_view(), name='group_delete'),
    #
    path('user/', UserListView.as_view(), name='user_index'),
    path('export/users', export_users, name='export_users'),
    path('print/users', print_users, name='print_users'),
    path('user/new', UserCreateView.as_view(), name='user_new'),
    path('user/<int:pk>/edit', UserUpdateView.as_view(), name='user_edit'),
    path('user/<int:pk>/delete', UserDeleteView.as_view(), name='user_delete'),
    path('user/<int:pk>/change-password', UserChangePassword, name='user_change_password'),
]
