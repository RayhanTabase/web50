import random
import markdown2

from django.shortcuts import render

from . import util
from .forms import WikiForm

from django.http import HttpResponseRedirect
from django.urls import reverse



def index_view(request):
    #print("index_view")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def add_view(request):
    #print("add_view")
    form = WikiForm()
    if request.method == "POST":

        form = WikiForm(request.POST)
        

        if form.is_valid():    
            upper_list = [x.upper() for x in util.list_entries()]   
            title = form.cleaned_data["title"]
            
            #print("form is valid")

            #save if title does not exist
            if not title.upper() in upper_list:
                content = form.cleaned_data["content"]
                util.save_entry(title,(content.encode('ascii')))
                #print("saved")
                return HttpResponseRedirect(f"http://127.0.0.1:8000/wiki/{title}") 
                
            #title already exists 
            else:
                #print("Name not available")
                return render(request,"encyclopedia/error.html",{

                    "message": f"Sorry {title.upper()} Already Exists In Directory",
                })
            
        else:        
            return render(request,"encyclopedia/error.html",{
                    "message": "Invalid Form Submission"
                })

    return render(request, "encyclopedia/add.html",{
                "form": form,
            })

def page_view(request,name):
    #print("page_view")
    can_edit = False

    if name == "random":
        can_edit = True
        random_page = random.choice(util.list_entries())
        page = markdown2.markdown(util.get_entry(random_page))
        name = random_page

    elif util.get_entry(name) == None :
        return render(request,"encyclopedia/error.html",{
                    "message": f"Sorry {name.upper()} Doest Not Exist"
                })

    else:
        can_edit = True
        page = markdown2.markdown(util.get_entry(name))

    return render(request,"encyclopedia/search.html",{
            "page": page,
            "initial_search": name,
            "can_edit": can_edit,
        })


def search_view(request):
    
    can_edit = False

    if 'q' in request.GET :
        print(request.GET['q'])
    
        upper_list = [x.upper() for x in util.list_entries()]

        if request.GET['q'].upper() in upper_list : 

            can_edit = True

            return render(request,"encyclopedia/search.html",{
                "page": markdown2.markdown(util.get_entry(request.GET['q'])),
                "initial_search": request.GET['q'],
                "can_edit": can_edit,
            })


        else:
            available = []
            for wiki in util.list_entries():
                if wiki.startswith(request.GET['q'].upper()):
                    available.append(wiki)

            if not available:        
                return render(request,"encyclopedia/error.html",{
                    "message": f"Sorry {request.GET['q'].upper()} Doest Not Exist",
                })

            else:
                return render(request,"encyclopedia/search.html",{

                    "wikis": available,
                    "initial_search": request.GET['q'],
                    "can_edit": can_edit,
                })
    else:
        return HttpResponseRedirect(reverse("encyclopedia:index"))


def edit_view(request):
    if request.method == 'GET':
        title = request.GET["old_content"]
        current_page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            'title':title,
            'content':current_page,
        })

    if request.method == 'POST':
        form = WikiForm(request.POST)

        if form.is_valid():   
            #print("form is valid") 
            
            title = form.cleaned_data["title"] 
            content = form.cleaned_data["content"]

            util.save_entry(title,(content.encode('ascii')))
            return HttpResponseRedirect(f"http://127.0.0.1:8000/wiki/{title}")
        
        else:
            #print("not valid")
            return render(request,"encyclopedia/error.html",{
                    "message": "Invalid Form Submission"
                })

        
        





