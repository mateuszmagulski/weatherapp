from django.urls import path, include

from . import views

urlpatterns = [ 
    path("", views.index, name="index"),
    path("delete/<int:pk>", views.delete_city, name="delete_city"),

    path("api", views.api_overviwe, name="api_overview"),
    path("api/list", views.api_list, name="api_list"),
    path("api/details/<int:pk>", views.api_details, name="api_details"),
    path("api/create", views.api_create, name="api_create"),
    path("api/update/<int:pk>", views.api_update, name="api_update"),
    path("api/delete/<int:pk>", views.api_delete, name="api_delete"),
]
