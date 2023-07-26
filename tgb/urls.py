from django.urls import path
from .views import message_list, dashboard, register, login_user, logout_user, update_command, delete_command
                    

urlpatterns = [
    path('', message_list, name='clients'),
    path('dashboard/', dashboard, name='dash'),
    path('register/', register, name='register'),
    path('login/', login_user , name='login'),
    path('logout/', logout_user , name='logout'),
    path('update-command/<int:pk>', update_command, name='update_command'),
    path('delete-command/<int:pk>', delete_command, name='delete_command'),
]
