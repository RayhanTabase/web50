import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User,Post,Comment
from .forms import PostForm,CommentForm
from .create_values import create_comments,create_posts,create_users,create_follow_like

POSTS_PER_PAGE =10

def index(request):
    return render(request, "network/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def createPost(request):
    if request.method == "POST":

        form = PostForm(request.POST)

        if form.is_valid():

            post = request.POST["new_post"]
            creator = request.user

            newPost = Post(creator = creator, post=post)
            newPost.save()

            #print("new post created")
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"network/error.html")

def send_posts_data(request,posts,data):
        page_number = data.get("page_number")

        #print(data)     
        p = Paginator(posts, POSTS_PER_PAGE)
        all_posts = p.get_page(page_number)


        if all_posts.has_next():
            next_page = all_posts.number + 1
        else:
            next_page = 0


        if all_posts.has_previous():
            prev_page = all_posts.number - 1
        else:
            prev_page = 0

        #print(next_page)
        #print(prev_page)

        return JsonResponse([[post.serialize() for post in all_posts],[{
                "has_next": all_posts.has_next() ,
                "has_previous":all_posts.has_previous(),
                "number":all_posts.number, 
                "num_pages":all_posts.paginator.num_pages,
                "next_page_number":next_page,
                "previous_page_number":prev_page,

            }]],safe=False)  

@csrf_exempt
def getPosts(request,posts):
    if not request.method == "PUT":
        return HttpResponseRedirect(reverse("index"))

    else:
        # print(f"getting posts {posts}")
        if posts == "ALL":
            all_posts = Post.objects.all().order_by("-pk")

        elif posts == "FOLLOWING":
            user = request.user
            users = request.user.following.all()

            all_posts = Post.objects.filter(creator__in=users).order_by("-pk")
        

        data = json.loads(request.body)
        return send_posts_data(request,all_posts,data)

@csrf_exempt
def profile_posts(request,profile_name):
    # print(f"get post {profile_name}")
    if not request.method == "PUT":
        return HttpResponseRedirect(reverse("index"))

    else:
        
        try:
            user = User.objects.get(username=profile_name)
            all_posts = Post.objects.filter(creator=user).order_by("-pk")
        
        except:
            return HttpResponseRedirect(reverse("index"))
        


        data = json.loads(request.body)

        return send_posts_data(request,all_posts,data)


@csrf_exempt
@login_required
def likePost(request,post_id):
    if request.method=="PUT":
        post = Post.objects.get(id=post_id)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            post.save()
            liked = False
           

        else:
            post.likes.add(request.user)
            post.save()
            liked = True

        num_likes = post.likes.count()

        return JsonResponse({"likes":num_likes,"liked":liked }, safe=False,status=201)


def profile_view(request,profile_name):
    return render(request,"network/profile.html")


#@login_required
def get_user(request):
    #print("get user")
    return JsonResponse({"user": f"{request.user.username}"}, safe=False)




@csrf_exempt
@login_required
def editPost(request,post_id):
    if request.method=="PUT":
        post = Post.objects.get(id=post_id)

        if request.user == post.creator:
            print("valid user")

            data = json.loads(request.body)
            new_post = data.get("new_post")

            form = PostForm(data)

            if form.is_valid():
                print("valid edit")

                post.post = new_post
                post.save()
                return HttpResponse(status=204)

            else:
                print("invalid edit")
                return HttpResponse(status=201)

        else:
            return HttpResponse(status=404)
    
@csrf_exempt
@login_required   
def follow(request,profile_name):
    # print(f"follow {profile_name}")
    if request.method=="PUT":
        profile = User.objects.get(username=profile_name)


        if request.user == profile:
            return HttpResponse(status=404)


        if request.user in profile.followers.all():
            profile.followers.remove(request.user)
            request.user.following.remove(profile)
            is_following = False
            
        else:
            profile.followers.add(request.user)
            request.user.following.add(profile)
            is_following = True

        profile.save()
        num_following= profile.followers.count()
    
        return JsonResponse({"num_following":num_following,"is_following":is_following }, safe=False,status=201)

    return HttpResponse(status=404)



@csrf_exempt
def profile_info(request,profile_name):
    #print(f"get profile info of {profile_name}")

    try:
        user = User.objects.get(username=profile_name)

        if request.user == user:
            #print("my_profile")
            return JsonResponse(user.serialize() , safe=False)

        #print("not my profile")
        
        return JsonResponse(user.serialize() , safe=False)

    except:
        return HttpResponse(status=404)

@login_required
@csrf_exempt
def createComment(request):
    if request.method == "POST":  
        # print("creating comment")
        data = json.loads(request.body)
        # print(data)

        post_id = data["post_id"]
        comment = data["comment"]
        # print(post_id,comment)

        form = CommentForm(data)
        if form.is_valid():
            post = Post.objects.get(id = post_id)

            new_comment = Comment(post = post, creator=request.user, comment = comment)

            new_comment.save()
            print("comment saved")
            return HttpResponse(status=204)

        else:
            return HttpResponse(status=201)





@csrf_exempt
def getComments(request):
    if request.method == "PUT":
        try:
                
            data = json.loads(request.body)

            post_id = data["post_id"]
            
            # print(post_id)

            post = Post.objects.get(id=post_id)
            print(post.post)
            
            comments = Comment.objects.filter(post=post).order_by("-pk")

        except:
            return HttpResponse(status=404)


        return JsonResponse([comment.serialize() for comment in comments],safe=False)



def dummy(request):
    # create_users(7)
    # create_posts(20)
    # create_comments(100)
    # create_follow_like(200)
    # return render(request, "network/index.html")
    return render(request,"network/index.html")
