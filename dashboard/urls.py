from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name="home"),
    path('load_work_items/', views.load_work_items, name="load_work_items"),
    path('create_webhook/', views.create_webhook, name="create_webhook"),
    path('workitem/<str:pk>/', views.workitem, name="workitem"),

    path('create_comment/<str:pk>/', views.create_comment, name="create_comment"),
    path('update_comment/<str:pk>/', views.update_comment, name="update_comment"),
    path('delete_comment/<str:pk>/', views.delete_comment, name="delete_comment"),

    path('update_in_DM/<str:pk>/', views.update_in_DM, name="update_in_DM"),
    path('update_hours/<str:pk>/', views.update_hours, name="update_hours"),
    path('update_ad_work_package/<str:pk>/', views.update_ad_work_package, name="update_ad_work_package"),

    path('create_IA/<str:pk>/', views.create_IA, name="create_IA"),
    path('create_CR/<str:pk>/', views.create_CR, name="create_CR"),
    path('bulkcreate_IA/', views.bulkcreate_IA, name="bulkcreate_IA"),
    path('reset_IA/', views.reset_IA, name="reset_IA"),

    path('download/IA/', views.download_ia, name="download_ia"),
    path('download/CR/', views.download_cr, name="download_cr"),
    path('download_ia/<str:filename>/', views.download_doc, name="download_doc"),
    path('download_cr/<str:filename>/', views.download_excel, name="download_excel")

]
