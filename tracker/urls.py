from django.urls import path
from . import views

urlpatterns = [
    

    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('marks/', views.marks_page, name='marks'),
    path('edit-mark/<int:id>/', views.edit_mark, name='edit_mark'),
    path('delete-mark/<int:id>/', views.delete_mark, name='delete_mark'),

    
    path('assignment/', views.assignment_page, name='assignment'),
    path('delete_assignment/<int:id>/', views.delete_assignment, name='delete_assignment'),
    path('complete_assignment/<int:id>/', views.complete_assignment, name='complete_assignment'),
    path("task/",views.task_page,name="task"),

    path("complete_task/<int:id>/",views.complete_task,name="complete_task"),

    path("delete_task/<int:id>/",views.delete_task,name="delete_task"),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
   
]   
