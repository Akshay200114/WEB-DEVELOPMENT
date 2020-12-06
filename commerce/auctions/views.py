from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from django import forms

class ListingForm(forms.Form):
    title= forms.CharField(
        max_length=64, 
        label="Item Title", 
        widget=forms.TextInput(attrs={'placeholder': "Title"})
    )
    description = forms.CharField(
            label="Item Description",
            max_length=256,
            widget=forms.Textarea(attrs={"class": "form-control",'placeholder': 'Enter Description here', "rows": "3"})
            )
    bid = forms.IntegerField(
            label="Initial Bid",
            widget=forms.TextInput(attrs={"class": "form-control", "type": "number",'placeholder': "Enter the IniTial Bid", "min": "0"})
            )
    image = forms.URLField(
            label="Item URL",
            required=False,
            widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Image Field"})
            )
    category = forms.CharField(
            label="Category",
            required=False,
            widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Enter The Category You want...."})
            )

def index(request):
    Listing=Create_Listing.objects.all()
    return render(request, "auctions/index.html",{'List': Listing})


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
            user = User.objects.create(username=username, email=email, password=password)
            user.save()
            login(request, user)
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login")
def create_new(request):
    msg=""
    current_user=User.objects.get(username=request.user.username)
    all_items_listing=[i.Title for i in Create_Listing.objects.all()]
    if request.method =="POST":
        form= ListingForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            img=form.cleaned_data['image']
            des=form.cleaned_data['description']
            initial_bid=form.cleaned_data['bid']
            category=form.cleaned_data['category']
            if title in all_items_listing:
                msg="This Item already exists"
            else:
                print("akshay")
                Model=Create_Listing(Title=title, bid=initial_bid, Image=img, Description=des, created_by=current_user)
                Model.save()
                new_cat=Category(cat_user=current_user, cat_item=Model, category=category)
                new_cat.save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'auctions/create.html',{
        'form':ListingForm(),
        'msg':msg
    })

@login_required(login_url="/login")
def show_list(request,title):
    current_user=User.objects.get(username=request.user.username)
    curr_listing=Create_Listing.objects.get(Title=title)
    comments=Comments.objects.filter(item_comment=curr_listing)
    watchlist_check=Watchlist.objects.filter(user_watchlist=current_user,watchlist=curr_listing)
    bids=[[str(i.user_bid), i.bid_value] for i in Bid.objects.filter(listing_bid=curr_listing)]
    if len(bids)!=0:
        greatest_bid=max(bids[len(bids)-1][-1], curr_listing.bid)
        greatest_user=bids[len(bids)-1][-2]
    else:
        greatest_bid=curr_listing.bid
        greatest_user=""
    if request.method == "POST":
        if "add_bid" in request.POST:
            bid=int(request.POST['bids'])
            if current_user.username in [i[0] for i in bids]:
                new_bid=Bid.objects.get(user_bid=current_user,listing_bid=curr_listing)
                new_bid.bid_value = bid
            else:
                new_bid=Bid(user_bid=current_user, listing_bid=curr_listing, bid_value=bid) 
            new_bid.save()
        if "addcomment" in request.POST:
            comment=request.POST['comment']
            if comment!='':
                new_comment=Comments(user_comment=current_user,item_comment=curr_listing, comment=comment)
                new_comment.save()
            else:
                return render(request, "auctions/listing.html" ,{
                    'message': "Enter The valid Comment here"
                })
        if "watchlist_add" in request.POST:
            new_watchlist=Watchlist(user_watchlist=current_user,watchlist=curr_listing)
            new_watchlist.save()
        if "watchlist_rm" in request.POST:
            watchlist_check.delete()
        if "close_List" in request.POST:
            curr_listing.active=False
            curr_listing.save()
                   
    return render(request, "auctions/listing.html", {
        'curr_listing': curr_listing,
        'current_user': current_user,
        'high_bid': greatest_bid,
        'comments': comments,
        'highest_bidder': greatest_user,
        'check': len(watchlist_check),
        'Comment': len(comments)
    })

@login_required(login_url='/login')    
def watchlist(request):
    current_user=User.objects.get(username=request.user.username)
    watchlist=Watchlist.objects.filter(user_watchlist=current_user)
    return render(request,'auctions/watchlist.html' ,{
        'watchlists':watchlist
    })

@login_required(login_url='/login')
def get_my_Listing(request):
    current_user=User.objects.get(username=request.user.username)
    created_user=Create_Listing.objects.filter(created_by=current_user)
    return render(request, "auctions/my_listing.html", {
        'listings': created_user
    })

