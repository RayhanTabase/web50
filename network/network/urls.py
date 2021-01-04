
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.index, name="following"),
    path("profile/<str:profile_name>", views.profile_view, name="profile"),

    
    #API
    path("profile/<str:profile_name>/follow", views.follow, name="follow_api"),
    path("profile/<str:profile_name>/profile_posts", views.profile_posts, name="profile_posts_api"),
    path("profile/<str:profile_name>/profile_info", views.profile_info, name="profile_info_api"),

    
    # API - POST
    path("createPost", views.createPost, name="createPost"),
    path("getPosts/<str:posts>", views.getPosts, name="getPosts"),
    path("likePost/<int:post_id>",views.likePost,name="like_api"),
    path("get_user",views.get_user,name="user_api"),
    path("editPost/<int:post_id>",views.editPost,name="edit_post_api"),


    #API - COMMENT
    path("createComment",views.createComment,name="create_comment"),
    path("getComments",views.getComments,name="get_comment"),


    ##########
    path("dummy",views.dummy),


]
