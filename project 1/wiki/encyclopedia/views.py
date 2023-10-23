from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown
import random
def convert_to_html(title):
    html = markdown.markdown(util.get_entry(title))
    return html

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/errorPage.html",{
            "title": title
        })
    return render(request, "encyclopedia/entry.html",{
            "title": title,
            "html": convert_to_html(title)
        })

def search(request):
    title = request.GET['q']
    if util.get_entry(title) != None:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "html": convert_to_html(title)
        })
    possible_titles = []
    entries = util.list_entries()
    for entry in entries:
        if entry.lower().__contains__(title.lower()):
            possible_titles.append(entry) 

    if len(possible_titles) == 0:
        return render(request, "encyclopedia/errorPage.html",{
            "title": title
        })
   
    return render(request, "encyclopedia/results.html", {
        "title": title,
        "entries": possible_titles
    })

def createPage(request):
    return render(request, "encyclopedia/createPage.html")

def new(request):
    title = request.GET['title']
    body = request.GET['body']
    if util.get_entry(title) != None:
        return render(request, "encyclopedia/pageExists.html",{
            "title":title
        })
    util.save_entry(title,body)
    return render(request, "encyclopedia/entry.html",{
            "title": title,
            "html": convert_to_html(title)
        })

def edit(request, title):
    return render(request, "encyclopedia/editPage.html",{
            "title": title,
            "body": util.get_entry(title)
        })

def save(request, title):
    body = request.GET['body']
    util.save_entry(title, body)
    return render(request, "encyclopedia/entry.html",{
            "title": title,
            "html": convert_to_html(title)
        })
    
def rand(request):
    ls = util.list_entries()
    rnd = random.randint(0,len(ls) - 1)
    title = ls[rnd]
    return render(request, "encyclopedia/entry.html",{
            "title": title,
            "html": convert_to_html(title)
        })
