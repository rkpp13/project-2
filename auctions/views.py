from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import *
from .forms import *

DefaultImage = "https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found.jpg"

def index(request):
    return render(request, "auctions/index.html", { 
        "auctions": Listing.objects.filter(status=True)
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
            user = User.objects.create_user(username.capitalize(), email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            # Me using walrus operator first time, it's nice :=
            if not bool(image := request.POST['image']): image = DefaultImage
            listing = Listing.objects.create(
                image=image,
                owner=request.user,
                title=form.cleaned_data["title"],
                category=form.cleaned_data["category"],
                description=form.cleaned_data["description"],
                startingbid=form.cleaned_data["StartingBid"],
            )
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {
        "form": ListingForm()
    })

def listing(request, id):
    user = request.user
    try:
        listing = Listing.objects.get(pk=id)
    except Listing.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    watchlist = True
    if user.is_authenticated:
        if user.watchlist.filter(id=id): watchlist = False

    bids_yet=lastbid=lastbidder=owner=False

    if listing.bids.all(): bids_yet=True; lastbid=listing.bids.last().bid; lastbidder=listing.bids.last().user
    if listing.owner==request.user : owner=True # I like one-liners :)

    return render(request, "auctions/listing.html", {
        "auction": listing,
        "watchlist": watchlist,
        "active": listing.status,
        "bids_yet": bids_yet,
        "owner": owner,
        "lastbid": lastbid,
        "lastbidder": lastbidder,
        "bidding__form": BidForm(),
        "comment__form": CommentForm(),
        "comments": reversed(listing.comments.all())
    })

@login_required(login_url='login')
def close(request, id):
    listing = Listing.objects.get(pk=id)
    if request.user == listing.owner:
        listing.status = False
        listing.save()
    return HttpResponseRedirect(reverse("listing", args=[id]))

@login_required(login_url='login')
def bid(request, id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            listing = Listing.objects.get(pk=id)
            bid = form.cleaned_data["bid"]

            message = False
            if (not listing.bids.all()) and (not (bid >= listing.startingbid)):
                message = "The bid must be at least as large as the <b>starting bid</b> !"
            elif listing.bids.all():
                if not (bid > listing.bids.last().bid):
                    message = "The bid must be greater than the <b>current bid</b> !"

            if bool(message):
                messages.error(request, message)
                return HttpResponseRedirect(reverse("listing", args=[id]))
            else:
                messages.success(request, 'Your Bid was Successful !')
                bid = Bid.objects.create(
                    user=request.user,
                    listing=listing,
                    bid=bid,
                )
    return HttpResponseRedirect(reverse("listing", args=[id]))

@login_required(login_url='login')
def comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            listing = Listing.objects.get(pk=id)
            comment = form.cleaned_data["comment"]
            comment = Comment.objects.create(
                user=request.user,
                listing=listing,
                comment=comment,
            )
    return HttpResponseRedirect(reverse("listing", args=[id]))

@login_required(login_url='login')
def watchlist(request):
    return render(request, "auctions/index.html", {
        "auctions": Listing.objects.filter(user=request.user)
    })

@login_required(login_url='login')
def watchlist_modify(request, id):
    wl = request.user.watchlist
    if wl.filter(id=id):
        wl.remove(id)
    else:
        wl.add(id)
    return HttpResponseRedirect(reverse("listing", args=[id]))

def category(request, category):
    return render(request, "auctions/index.html", {
        "auctions": Listing.objects.filter(status=True,category=category)
    })
