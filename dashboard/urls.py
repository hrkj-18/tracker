from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.load_work_items, name="load_work_items"),
    path('workitem/<str:pk>/', views.workitem, name="workitem"),

    path('create_comment/<str:pk>/', views.create_comment, name="create_comment"),
    path('update_comment/<str:pk>/', views.update_comment, name="update_comment"),
    path('delete_comment/<str:pk>/', views.delete_comment, name="delete_comment"),

    path('create_IA/<str:pk>/', views.create_IA, name="create_IA"),
    path('create_CR/<str:pk>/', views.create_CR, name="create_CR"),
    path('bulkcreate_IA/', views.bulkcreate_IA, name="bulkcreate_IA")
]