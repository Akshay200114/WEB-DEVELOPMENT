from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create/', views.create_new, name="create"),
    path('listinfo/<str:title>',views.show_list, name='show'),
    path('watchlist',views.watchlist, name='watchlist'),
    path('my_listings', views.get_my_Listing, name="my_listings")
]
