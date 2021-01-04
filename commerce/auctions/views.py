from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Bid
from .forms import Listing_form, Comment_form, Bid_form

CATEGORIES =["Fashion","Sports","Toys","Home","Utensils","Electronics","Other"]


def index_view(request):
    active_listings = Listing.objects.all().filter(active=True).order_by('item_name')

    listings = active_listings.annotate(highest_bid=Max('bid_item__bid'))

    #displays all active listings from the listings model
    return render(request, "auctions/index.html",{
        "title": "All Listings",
        "categories":CATEGORIES,
        "Active_Listings": listings,
    })


def category_view(request,category):
    if category in CATEGORIES:
        try:
            active_listings = Listing.objects.filter(category=category,active=True).order_by('item_name')
            listings = active_listings.annotate(highest_bid=Max('bid_item__bid'))
        except:
            return render(request,"auctions/error.html")

    return render(request, "auctions/index.html",{
        "title": category,
        "categories":CATEGORIES,
        "Active_Listings": listings,
    })

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing_view(request,listing_id):  
    all_comments =[]
    try:
        item = Listing.objects.get(id=listing_id)
    except:
        return render(request,"auctions/error.html")
    
    #get comments
    if item:
        get_comments = Comment.objects.all()
        for comment in get_comments:
            if comment.cmt_item.item_name == item.item_name:
                all_comments.append(comment)
    else:
        comments = None 
        
    #bids query
    bids = Bid.objects.all().filter(item=item)
    bid_values = [bid.bid for bid in bids]
    
    if not bid_values:
        highest = float(item.bid_price)
        min_bid = highest
    else:
        #print(bid_values)
        highest = float(max(bid_values)) 
        min_bid = highest + 0.01
    #print(highest)

    watched = False
    
    return render(request, "auctions/listing_page.html",{
        "listing":item,
        "comments": all_comments,
        "highest_bid":highest,
        "min_bid": min_bid,
        "num_bids": bids.count(),
        "watched": watched,
    })
    

@login_required
def comment_view(request): 

    #create new comment
    if request.method == "POST":
        form = Comment_form(request.POST)

        if form.is_valid():
            print("valid comment")
            listing_id = int(request.POST["listing_id"])
            item = Listing.objects.get(id=listing_id)
            comment = form.cleaned_data["comment"]

            new_comment = Comment(creator=request.user,cmt_item = item,comment = comment)
            new_comment.save()
            return redirect(f'listing/{listing_id}')

    #print("invalid comment")
    return render(request,"auctions/error.html")
        
@login_required
def create_listing_view(request):
    
    if request.method =="POST":
        form = Listing_form(request.POST)

        if form.is_valid():
            #print("creating new listing")
            try:
                new_listing = Listing(creator=request.user,item_name=form.cleaned_data["listing_name"],item_description=form.cleaned_data["listing_description"],image=form.cleaned_data["listing_image"], category=form.cleaned_data["listing_category"] ,bid_price=form.cleaned_data["starting_bid"])
                new_listing.save()
                return redirect(f'listing/{new_listing.id}')
            except:
                #print("failed to create listing")
                return render(request,"auctions/error.html")
        else:
            #print("invalid form")
            return render(request,"auctions/error.html")
           

    return render(request, "auctions/create_listing.html",{
            "categories": CATEGORIES
        })

@login_required
def submit_bid_view(request):

    if request.method =="POST":

        form = Bid_form(request.POST)
    
        if form.is_valid():
            listing=Listing.objects.get(id=request.POST["listing_id"])
            
            new_bid = Bid(bidder= request.user,item=listing,bid = form.cleaned_data["bid"])  
            new_bid.save() 
            
            return redirect(f'listing/{listing.id}')

        else:
            print("invalid form-Bid")
            return render(request,"auctions/error.html")
      
    


@login_required
def close_auction_view(request):
    
    listing_id = request.POST["listing_id"]
    listing = Listing.objects.get(id=listing_id)
    if listing.creator != request.user:
        return render(request,"auctions/error.html")

    try:
        listing.active = False
        #print("L-inactive")
        my_bids = Bid.objects.all().filter(item=listing)

        if my_bids:

            highest_bids={"highest_bid": ( bid.bidder,bid.bid) for bid in my_bids}

            bidder = (highest_bids["highest_bid"][0])

            #get highest bid and set winner to bidder
            
            listing.winner = bidder
            #print("L-winner")
            listing.save()
        else:
            listing.winner = None
            #print("L-no winner")
            listing.save()

        return redirect(f'listing/{listing_id}')
        
    except:
        return render(request,"auctions/error.html")


@login_required
def watch_list_view(request):

    if request.method == "POST":
        listing = Listing.objects.get(id=request.POST["listing_id"])
        user = request.user

        if listing in user.watchlist.all():
            user.watchlist.remove(listing)
        else:
            user.watchlist.add(listing) 
        #
        user.save()
        return redirect(f'listing/{listing.id}')

    else:
        return render(request,"auctions/error.html")




@login_required
def listing_group_view(request,group_type):

    if group_type == "my_bids":
        print("my_bids")
        user = request.user
        my_bids = Bid.objects.all().filter(bidder=user)
        print(my_bids)
        my_highest_bids={bid.item.item_name:(bid.bid,bid.item) for bid in my_bids}
        #print(my_highest_bids)  
        return render(request,"auctions/bids_placed.html",{
            "my_bids": my_highest_bids,
        })

    elif group_type == "watchlist":
        print("watchlist")
        title = "Watch List"
        listings = request.user.watchlist.all()
        

    elif group_type == "my_listings":
        print("my_listings")
        title = "My Listings"
        listings = Listing.objects.filter(creator=request.user).order_by("-active")

    else:
        return render(request,"auctions/error.html")

    return render(request, "auctions/index.html",{
        "title":title,
        "Active_Listings": listings.annotate(highest_bid=Max('bid_item__bid')),
    })


@login_required
def checkout_view(request):
    user = request.user

    #filter all winning bids
    won_bids = Listing.objects.filter(winner=user).annotate(highest_bid=Max('bid_item__bid'))

    return render(request,'auctions/checkout.html',{
        "won_bids": won_bids
    })
        




        
'''
@login_required
def edit_listing_view(request):
    highest_bids= None
    winning_bid = None

    if request.method =="GET":
        listing_id = request.GET["listing_id"]
        #print(listing_id)
    
        #get the listing
        listing = Listing.objects.get(id=listing_id)
        #print(listing)
        
        if listing.active:
            #get highest bid
            my_bids = Bids.objects.all().filter(item=listing)
            highest_bids={"highest_bid": ( bid.bidder.id,bid.bidder.username,bid.bid) for bid in my_bids}
            
        else:
            winner = listing.winner
            #print(winner)
            winner_bids = Bids.objects.all().filter(bidder=winner)
            winning_bid =[bid.bid for bid in winner_bids]

            if winning_bid:
                winning_bid=max(winning_bid)
            else:
                winning_bid = None

        if not highest_bids:
            highest_bids={"highest_bid": ( None,None,None)}
        
        return render(request,"auctions/edit_listing.html",{
            "listing": listing,
            "highest_bid": highest_bids,
            "winning_bid": winning_bid,
            "categories": CATEGORIES
        })


@login_required
def delete_listing_view(request):
    pass
'''
    