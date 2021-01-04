from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("category/<str:category>", views.category_view, name="category"),
    path("listing/<int:listing_id>",views.listing_view,name="listing"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #login required
    path("listing/<str:group_type>",views.listing_group_view,name="group_type"),
    path("create_listing",views.create_listing_view,name="create_listing"),
  
    path("checkout",views.checkout_view,name="checkout"), 
    #path("edit_listing",views.edit_listing_view,name="edit_listing"), 

    path("comment",views.comment_view,name="comment"),
    path("watch_list",views.watch_list_view,name="watch_list"), 
    path("bid",views.submit_bid_view,name="bid"),
    path("close_auction",views.close_auction_view,name="close_auction"),
    
]
