from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect

from .models import *


def index(request):
    return render(
        request,
        "auctions/index.html",
        {
            "listings": Listing.objects.filter(available="True"),
        },
    )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def add_listing(request):
    return render(
        request,
        "auctions/addListing.html",
        {
            "categories": Category.objects.all(),
        },
    )


def viewcategory(request, name):
    if Category.objects.filter(name=name).exists() and name != "None":
        return render(
            request,
            "auctions/index.html",
            {
                "listings": Listing.objects.filter(
                    available="True", category=name
                ).values()
            },
        )
    else:
        return render(
            request,
            "auctions/categoriesList.html",
            {"categories": Category.objects.all(), "error": True, "name": name},
        )


def categories(request):
    return render(
        request,
        "auctions/categoriesList.html",
        {
            "categories": Category.objects.all(),
            "error": False,
            "name": "none",
        },
    )


def save_entry(request, Uid):
    title = request.POST["title"]
    description = request.POST["description"]
    bid = request.POST["bid"]
    url = request.POST["url"]
    min_bid = int(bid) + 1
    category = Category.objects.get(name=request.POST["category"])
    username = User.objects.get(id=Uid).username

    Listing.objects.create(
        title=title,
        description=description,
        current_bid=bid,
        available=True,
        pic_url=url,
        category=category,
        user_id=Uid,
        user_username=username,
        bids=0,
        bid_winner="None",
        min_bid=min_bid,
    )

    return render(
        request,
        "auctions/saved.html",
        {"title": title},
    )


def view_listing(request, Lid, Uid):
    watchlist = Watchlist.objects.filter(user_id=Uid, listing_id=Lid).count()
    return render(
        request,
        "auctions/viewListing.html",
        {
            "listing": Listing.objects.filter(id=Lid)[0],
            "comments": Comment.objects.filter(listing_id=Lid),
            "watchlist": watchlist,
        },
    )


def comment(request, Lid, Uid):
    body = request.POST["body"]
    if len(body) > 0:
        user = User.objects.get(id=Uid)
        user_id = user.id
        user_username = user.username
        listing_id = Lid
        Comment.objects.create(
            body=body,
            user_id=user_id,
            user_username=user_username,
            listing_id=listing_id,
        )
    return redirect("view_listing", Lid=Lid, Uid=Uid)


def delcomment(request, Cid, Lid):
    Uid = Comment.objects.get(id=Cid).user_id
    Comment.objects.filter(id=Cid).delete()
    return redirect("view_listing", Lid=Lid, Uid=Uid)


def placebid(request, Uid, Lid):
    user = User.objects.get(id=Uid)
    tmp = Listing.objects.get(id=Lid)
    bid = request.POST["bid"]
    user_id = Uid
    user_username = user.username
    listing_id = Lid
    Bid.objects.create(
        user_id=user_id, user_username=user_username, listing_id=listing_id, bid=bid
    )
    tmp.bids = int(tmp.bids) + 1
    tmp.current_bid = bid
    tmp.bid_winner = user_username
    tmp.min_bid = int(bid) + 1

    tmp.save()
    return redirect("view_listing", Lid=Lid, Uid=Uid)


def closebid(request, Lid):
    listing = Listing.objects.get(id=Lid)
    bid = listing.current_bid
    if listing.bids != 0:
        bidObj = Bid.objects.get(
            user_username=listing.bid_winner, listing_id=listing.id, bid=bid
        )
        user_username = listing.bid_winner
        listing_id = Lid
        closeBid.objects.create(
            user_id=bidObj.user_id,
            user_username=user_username,
            listing_id=listing_id,
        )
    listing.available = "False"
    listing.save()
    return render(
        request,
        "auctions/closed.html",
        {"listing": listing},
    )


def viewWatchlist(request, Uid):
    return render(
        request,
        "auctions/viewwatchlist.html",
        {
            "Watchlist": Watchlist.objects.filter(user_id=Uid),
        },
    )


def addWatchlist(request, Uid, Lid):
    user_id = Uid
    user_username = User.objects.get(id=Uid).username
    listing = Listing.objects.get(id=Lid)
    if Watchlist.objects.filter(user_id=Uid, listing_id=Lid).count() == 0:
        Watchlist.objects.create(
            user_id=user_id,
            user_username=user_username,
            listing_id=listing.id,
            title=listing.title,
            pic_url=listing.pic_url,
        )
    return redirect("view_listing", Lid=Lid, Uid=Uid)


def removeWatchlist(request, Uid, Lid, flag):
    Watchlist.objects.get(user_id=Uid, listing_id=Lid).delete()
    if flag:
        return redirect("viewWatchlist", Uid=Uid)
    return redirect("view_listing", Lid=Lid, Uid=Uid)


def closed(request):
    return render(
        request,
        "auctions/closedListing.html",
        {
            "listings": Listing.objects.filter(available="False"),
        },
    )
