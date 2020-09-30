from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("c/<category>", views.category, name="c"),
    path("listing/<id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<id>", views.watchlist_modify, name="modify"),
    path("comment/<id>", views.comment, name="comment"),
    path("close/<id>", views.close, name="close"),
    path("bid/<id>", views.bid, name="bid"),
]
