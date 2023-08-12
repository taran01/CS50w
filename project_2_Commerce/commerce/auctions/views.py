from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *


class Newlisting_form(forms.Form):
    CATEGORY_CHOICES = [("", "-- Select a Category --")]
    CATEGORY_CHOICES = CATEGORY_CHOICES + [(item.id, item.category) for item in Category.objects.all()]

    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea)
    starting_price = forms.DecimalField(min_value=1)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, initial="")
    img_url = forms.CharField(max_length=250)


class Bid_form(forms.Form):
    bid = forms.DecimalField(min_value=1, label="", widget=forms.NumberInput(attrs={'placeholder': 'Bid'}))


class Comment_form(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Write something...", "style": "height: 100px;"}), label="Add a comment")

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(status=True),
        "title": "Active Listings"
    })


def closed_listings(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(status=False),
        "title": "Closed Listings"
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
            if "next" in request.POST:
                return HttpResponseRedirect(request.POST["next"])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        next = request.GET.get('next', False)
        return render(request, "auctions/login.html", {
            "next": next
        })


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


def listing_details(request, id):
    try:
        listing = Listing.objects.get(pk=id)
    except:
        return HttpResponseRedirect(reverse("index"))

    if not request.user.is_authenticated:
        watchlist = None
    else:
        watchlist = listing.watchlist.filter(user=request.user)

    comments = listing.comments.all()

    return render(request, "auctions/listing-details.html", {
        "listing": listing,
        "bid_form": Bid_form(),
        "comment_form": Comment_form(),
        "bids": Bid.objects.filter(listing_id=id),
        "watchlist": watchlist,
        "comments": comments
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category_listings(request, id):
    try:
        category = Category.objects.get(pk=id)
    except:
        return HttpResponseRedirect(reverse("categories"))
    listings = category.listings.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "title": f"Category: {category}"
    })


@login_required(login_url="/login")
def new_listing(request):
    # cat = list(Category.objects.values_list("category", flat=True))
    # cat = [("default", "Select a Category"), *((item.category, item.category) for item in Category.objects.all())]
    if request.method == "POST":
        form = Newlisting_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_price = form.cleaned_data["starting_price"]
            img_url = form.cleaned_data["img_url"]
            category = Category.objects.get(pk=int(form.cleaned_data["category"]))
            owner = User.objects.get(pk=int(request.user.id))

            listing = Listing(title=title, description=description, starting_price=starting_price, img_url=img_url, category=category, owner=owner)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/newlisting.html", {
                "form": form
            })

    else:
        return render(request, "auctions/newlisting.html", {
            "form": Newlisting_form()
        })


@login_required(login_url="/login")
def bid(request, id):
    if request.method == "POST":
        user = User.objects.get(pk=int(request.user.id))
        try:
            listing = Listing.objects.get(pk=id)
        except:
            return HttpResponseRedirect(reverse("index"))

        watchlist = listing.watchlist.filter(user=request.user)
        comments = listing.comments.all()

        form = Bid_form(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            if bid >= float(listing.starting_price) and (listing.current_bid == None or bid > float(listing.current_bid.bid_amount)):
                newbid = Bid(user=user, listing=listing, bid_amount=bid)
                newbid.save()
                listing.current_bid = newbid
                listing.save()
                return HttpResponseRedirect(reverse("listing_details", args=(listing.id,)))
            else:
                return render(request, "auctions/listing-details.html", {
                    "listing": listing,
                    "bid_form": form,
                    "comment_form": Comment_form(),
                    "bids": Bid.objects.filter(listing_id=id),
                    "watchlist": watchlist,
                    "comments": comments,
                    "message": "Please provide bid greater than current bid or starting price."
                })

        else:
            return render(request, "auctions/listing-details.html", {
                "listing": listing,
                "bid_form": form,
                "comment_form": Comment_form(),
                "bids": Bid.objects.filter(listing_id=id),
                "watchlist": watchlist,
                "comments": comments,
                "message": "Invalid bid"
            })

    else:
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def watchlist(request, id):
    if request.method == "POST":
        user = User.objects.get(pk=int(request.user.id))
        try:
            listing = Listing.objects.get(pk=id)
        except:
            return HttpResponseRedirect(reverse("index"))

        check = Watchlist.objects.filter(user=user, listing=listing)
        if not check:
            watchlist = Watchlist.objects.create()
            watchlist.user.add(user)
            watchlist.listing.add(listing)
            return HttpResponseRedirect(reverse("listing_details", args=(listing.id,)))
        else:
            check.delete()
            return HttpResponseRedirect(reverse("listing_details", args=(listing.id,)))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def watchlist_items(request):
    user = User.objects.get(pk=int(request.user.id))
    listings = []
    watchlists = user.watchlist.all()
    for watchlist in watchlists:
        listings.extend(watchlist.listing.all())
    return render(request, "auctions/index.html", {
        "listings": listings,
        "title": f"{user.username}'s Watchlist"
    })


@login_required(login_url="/login")
def close_listing(request, id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(pk=id)
        except:
            return HttpResponseRedirect(reverse("index"))

        if request.user == listing.owner:
            listing.status = False
            listing.save()
        return HttpResponseRedirect(reverse("listing_details", args=(listing.id,)))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def comments(request, id):
    if request.method == "POST":
        user = User.objects.get(pk=int(request.user.id))
        try:
            listing = Listing.objects.get(pk=id)
        except:
            return HttpResponseRedirect(reverse("index"))

        watchlist = listing.watchlist.filter(user=request.user)
        comments = listing.comments.all()

        form = Comment_form(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            comment = Comment(user=user, listing=listing, text=text)
            comment.save()
            return HttpResponseRedirect(reverse("listing_details", args=(listing.id,)))
        else:
            return render(request, "auctions/listing-details.html", {
                    "listing": listing,
                    "bid_form": Bid_form(),
                    "comment_form": form,
                    "bids": Bid.objects.filter(listing_id=id),
                    "watchlist": watchlist,
                    "comments": comments,
                    "comment_message": "Invaid comment input."
                })

    else:
        return HttpResponseRedirect(reverse("index"))