from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from . import util
import markdown2
from random import randrange

class ContactForm(forms.Form):
    title=forms.CharField(max_length=100, label="Title", widget=forms.TextInput(attrs={'placeholder':"Enter the title"}), required=True)
    Content= forms.CharField(widget=forms.Textarea(attrs={'row':4,'cols':15,'placeholder':"Enter the Markdown Content here"}),required=True, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
#This is to create the entries in the wiki.
def create(request):
    entries=util.list_entries()
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            content=form.cleaned_data['Content']
            if title in entries:
                Error="Title already exists!"
                return render(request, 'encyclopedia/create.html',{'form':ContactForm(),'error': Error})
            else:
                util.save_entry(title, content)
                return render(request, 'encyclopedia/saved.html', {
                    'title': title,
                    'content':markdown2.markdown(util.get_entry(title))               
                })
        else: 
            return HttpResponse("<h1> Invalid  form </h1> ")
    return render(request, "encyclopedia/create.html", {'form': ContactForm()})

#To get the entries in the html format.
def get_page(request, title):
    entries=util.list_entries()
    if title.capitalize() in entries:
        return render(request,'encyclopedia/saved.html', {
                'title': title,
                'content': markdown2.markdown(util.get_entry(title))
        })
    else:
        return render(request, 'encyclopedia/existence.html',{
            'error':f"The given title i.e ({title}) doesn't exists"
        })

#To Edit the entries
def edit(request):
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            title= form.cleaned_data['title']
            content= form.cleaned_data['Content']
            util.save_entry(title, content)
            return render(request, 'encyclopedia/saved.html', {
                'title': title,
                'content': markdown2.markdown(util.get_entry(title))
            }) 
    title=request.GET.get('title')
    content=util.get_entry(title)
    return render(request, 'encyclopedia/edit.html',{
        'editform': ContactForm(initial={'title':title,'Content': content})
     })  
# to get the random Pages.
def random(request):
    entries=util.list_entries()
    if len(entries)!=0:
        rand=randrange(len(entries))
        title=entries[rand]
        return render( request, 'encyclopedia/saved.html',{
            'title':title,
            'content': markdown2.markdown(util.get_entry(title))
        })
#To find the encyclopedia.
def search(request):
    entries=util.list_entries()
    title=request.GET.get('q')
    result=[res for res in entries if (title.capitalize() or title) in res]
    if len(result)!=0:
        if title in entries:
            return render(request, 'encyclopedia/saved.html',{
                'title':title,
                'content':markdown2.markdown(util.get_entry(title))
            })
        else:
            return render(request, 'encyclopedia/similar.html',{
                'entries': result,
                'similar':f" Similar results are Found for this ({title})."
            })
    else:
        return render(request,'encyclopedia/similar.html',{
            'error':f"No results Found"
        })
    


       

