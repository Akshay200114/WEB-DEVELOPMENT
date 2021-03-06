from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path('wiki/<str:title>',views.get_page, name='get_page'),
    path('edit', views.edit, name='edit'),
    path('random', views.random, name='random'),
    path('search/', views.search, name='search')
]
