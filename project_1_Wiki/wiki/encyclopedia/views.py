from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms

import random
import markdown2

from . import util

class newpage_form(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea())

class edit_form(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput())
    content = forms.CharField(widget=forms.Textarea())


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def query(request, title):
    entry = util.get_entry(title)
    try:
        html = markdown2.markdown(entry)
    except:
        html = "<h1>Error 404:</h1><br><h2>Sorry, your requested page could not be found.<h2>"
        title = "Not Found"
    return render(request, "encyclopedia/query.html", {
        "html": html,
        "title": title
    })


def search(request):
    q = request.GET["q"]
    if not q.isupper():
        q = q.capitalize()
    if util.get_entry(q):
        return HttpResponseRedirect(f"/wiki/{q}")
    else:
        all_entries = util.list_entries()
        q = q.lower()
        found_entries = []
        for entry in all_entries:
            if q in entry.lower():
                found_entries.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": found_entries,
            "q": q
        })


def new_page(request):
    if request.method == "POST":
        form = newpage_form(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/newpage.html", {
                    "error": "<h4>Error: Sorry, page already exists.</h4>"
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })

    return render(request, "encyclopedia/newpage.html", {
        "form": newpage_form()
    })


def random_page(request):
    entries = util.list_entries()
    page = random.choice(entries)
    return HttpResponseRedirect(f"/wiki/{page}")


def edit_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        data = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "form": edit_form(initial={"content": data, "title": title}),
            "title": title
        })
    else:
        return HttpResponseRedirect("/")


def save_page(request):
    if request.method == "POST":
        form = edit_form(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
    else:
        return HttpResponseRedirect("/")    