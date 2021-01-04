import random 
from .models import User,Post,Comment

def create_users(num):
    usernames =[]
    user_options =["John","Ama","Smith","Kwabena","Kofi","Akosua","Damata"]
    num_users = int(num/2)
    if num_users % 2:
        user_count = num_users
    else:
         user_count = num_users + 1

    for  count in range(0,user_count):
        code = random.randint(1,100)
        user = f"{random.choice(user_options)}{code}"
        usernames.append(user)

    for count in range(0,num):

        username= random.choice(usernames)
        password = f"{username}123"
        email= f"{username}@{username}.com"

        try:
            user = User(username=username,email=email,password=password)
            user.save()
        except:
            print("skipped user")
            # continue
            
        
   

def create_posts(num):
    users = User.objects.all()
    for count in range(0,num):
        creator = random.choice(users)
        post_text = f" this is a dummy post created using {creator} account"
        post = Post(creator=creator, post = post_text)
        post.save()


def create_comments(num):
    users = User.objects.all()
    posts = Post.objects.all()
    for count in range(0,num):
        creator = random.choice(users)
        post = random.choice(posts)
        comment = f"this is a dummy post created using {creator} account on"
        comment = Comment(post=post,creator=creator,comment=comment)
        comment.save()


def create_follow_like(num):
    users = User.objects.all()
    posts = Post.objects.all()

    for count in range(0,num):
        post = random.choice(posts)
        user = random.choice(users)

        try:
            follower = random.choice(users)
            if not user == follower:

                user.following.add(follower)
                
                follower.followers.add(user)
                user.save()
                follower.save()

                post.likes.add(follower)
                post.save()
        except:
            print("skip follow like")
            # continue
              
