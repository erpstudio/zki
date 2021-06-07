from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from .models import AreaZone

from django import forms
import django_tables2 as tables
import sweetify


class AreaZoneForm(forms.ModelForm):
    class Meta:
        model = AreaZone
        fields = ('name', 'description')
        widgets = {
                'name': forms.TextInput(attrs={'placeholder': _('Name')}),
                # 'AreaZone': forms.Select(attrs={'class': 'select2', 'width':'100%'})
        }
    

ACTIONS = '''
   <div class="btn-group"> 
   <a class="btn btn-primary" href="{% url 'areazone.update' record.id %}">Edit</a>
   <a class="btn btn-info" href="{% url 'areazone.show' record.id %}">View</a>
   <a class="btn btn-danger" href="{% url 'areazone.delete' record.id %}">Delete</a>
   </div>
'''

class AreaZoneTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    class Meta:
        model = AreaZone
        fields = ('name', 'description')


page_title = _("AreaZone")


# Create your views here.
def index(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add AreaZone", "link":"areazone.add"}
    page["nav_links"]["list"] = { "label":"AreaZone List", "link":"areazone.list"}
    return render(request, 'layout/bootstrap.html', {"page":page})


def add(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add AreaZone", "link":"areazone.add"}
    page["nav_links"]["list"] = { "label":"AreaZone List", "link":"areazone.list"}
    page["add"] = {}
    page["add"]["type"] = "form"
    page["add"]["action"] = "areazone.save"
    page["add"]["method"] = "post"
    page["add"]["title"] = _("Add AreaZone")
    page["add"]["form"] = AreaZoneForm()
    
    return render(request, 'layout/bootstrap.html', {"page":page})


def list(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add AreaZone", "link":"areazone.add"}
    page["nav_links"]["list"] = { "label":"AreaZone List", "link":"areazone.list"}
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("AreaZone List")
    page["list"]["table"] = AreaZoneTable(AreaZone.objects.all())
    
    return render(request, 'layout/bootstrap.html', {"page":page, "page_title":page_title})

def show(request, id):

    instance = AreaZone.objects.get(id=id)

    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add AreaZone", "link":"areazone.add"}
    page["nav_links"]["list"] = { "label":"AreaZone List", "link":"areazone.list"}
    page["profile"] = {}
    page["profile"]["type"] = "profile"
    page["profile"]["title"] = instance.name
    page["profile"]["slogan"] = instance.description
    
    data = {}
    page["profile"]["data"] = data

    return render(request, 'layout/bootstrap.html', {"page":page})


def save(request):
    if request.method == "POST":
        form = AreaZoneForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            sweetify.success(request, _('Saved Successfull'), timer=1000)
    
    
    return redirect('areazone.add')


def update(request, id):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add AreaZone", "link":"areazone.add"}
    page["nav_links"]["list"] = { "label":"AreaZone List", "link":"areazone.list"}
    page["update"] = {}
    page["update"]["type"] = "form"
    page["update"]["action"] = "areazone.update"
    page["update"]["record_id"] = id
    page["update"]["method"] = "post"
    page["update"]["title"] = _("Edit AreaZone")
    
    instance = AreaZone.objects.get(id=id)
    form = AreaZoneForm(request.POST or None, instance=instance)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            sweetify.success(request, _('Updated Successfull'), timer=1000)
            return redirect('areazone.update', id = id)
        else:
            sweetify.success(request, _('Action Error'), timer=1000)
    
    
    page["update"]["form"] = form
    return render(request, 'layout/bootstrap.html', {"page":page})


def delete(request, id):
    AreaZone.objects.filter(id=id).delete()
    sweetify.success(request, _('Deleted Successfull'), timer=1000)
    return redirect('areazone.list')