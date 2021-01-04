from django.urls import path

from . import views
app_name = "encyclopedia"

urlpatterns = [
    path('', views.index_view, name="index"),
    path('add/', views.add_view, name="add"),
    path('search/', views.search_view, name="search"),
    path('edit/',views.edit_view, name="edit"),
    path('<str:name>/', views.page_view, name="page"),
]
