from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new"),
    path("listings/<int:id>", views.listing_details, name="listing_details"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("categories", views.categories, name="categories"),
    path("category/<int:id>", views.category_listings, name="category_listings"),
    path("watchlist/<int:id>", views.watchlist, name="watchlist"),
    path("watchlist", views.watchlist_items, name="watchlists"),
    path("close/<int:id>", views.close_listing, name="close_listing"),
    path("closed", views.closed_listings, name="closed_listings"),
    path("comments/<int:id>", views.comments, name="comments")
]
