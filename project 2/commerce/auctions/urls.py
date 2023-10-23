from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closed", views.closed, name="closed"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("viewcategory/<str:name>", views.viewcategory, name="viewcategory"),
    path("addlisting", views.add_listing, name="add_listing"),
    path("save/<int:Uid>", views.save_entry, name="save"),
    path("viewlisting/<int:Lid>/<int:Uid>", views.view_listing, name="view_listing"),
    path("comment/<int:Lid>/<int:Uid>", views.comment, name="comment"),
    path("delcomment/<int:Cid>/<int:Lid>", views.delcomment, name="delcomment"),
    path("placebid/<int:Uid>/<int:Lid>", views.placebid, name="placeBid"),
    path("closebid/<int:Lid>", views.closebid, name="closeBid"),
    path("addWatchlist/<int:Uid>/<int:Lid>", views.addWatchlist, name="addWatchlist"),
    path(
        "removeWatchlist/<int:Uid>/<int:Lid>/<int:flag>",
        views.removeWatchlist,
        name="removeWatchlist",
    ),
    path("viewWatchlist/<int:Uid>", views.viewWatchlist, name="viewWatchlist"),
]
