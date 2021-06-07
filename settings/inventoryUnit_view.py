from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from .models import InventoryUnits

from django import forms
import django_tables2 as tables
import sweetify


class InventoryUnitsForm(forms.ModelForm):
    class Meta:
        model = InventoryUnits
        fields = ('name', 'description')
        widgets = {
                'name': forms.TextInput(attrs={'placeholder': _('Name')}),
                # 'Unit': forms.Select(attrs={'class': 'select2', 'width':'100%'})
        }
    

ACTIONS = '''
   <div class="btn-group"> 
   <a class="btn btn-primary" href="{% url 'inventory.unit.update' record.id %}">Edit</a>
   <a class="btn btn-info" href="{% url 'inventory.unit.show' record.id %}">View</a>
   <a class="btn btn-danger" href="{% url 'inventory.unit.delete' record.id %}">Delete</a>
   </div>
'''

class InventoryUnitsTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    class Meta:
        model = InventoryUnits
        fields = ('name', 'description')


page_title = _("Inventory Unit")


# Create your views here.
def index(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Unit", "link":"inventory.unit.add"}
    page["nav_links"]["list"] = { "label":"Unit List", "link":"inventory.unit.list"}
    return render(request, 'layout/bootstrap.html', {"page":page})


def add(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Unit", "link":"inventory.unit.add"}
    page["nav_links"]["list"] = { "label":"Unit List", "link":"inventory.unit.list"}
    page["add"] = {}
    page["add"]["type"] = "form"
    page["add"]["action"] = "inventory.unit.save"
    page["add"]["method"] = "post"
    page["add"]["title"] = _("Add Unit")
    page["add"]["form"] = InventoryUnitsForm()
    
    return render(request, 'layout/bootstrap.html', {"page":page})


def list(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Unit", "link":"inventory.unit.add"}
    page["nav_links"]["list"] = { "label":"Unit List", "link":"inventory.unit.list"}
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("Unit List")
    page["list"]["table"] = InventoryUnitsTable(InventoryUnits.objects.all())
    
    return render(request, 'layout/bootstrap.html', {"page":page, "page_title":page_title})

def show(request, id):

    instance = InventoryUnits.objects.get(id=id)

    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Unit", "link":"inventory.unit.add"}
    page["nav_links"]["list"] = { "label":"Unit List", "link":"inventory.unit.list"}
    page["profile"] = {}
    page["profile"]["type"] = "profile"
    page["profile"]["title"] = instance.name
    page["profile"]["slogan"] = instance.description
    
    data = {}
    page["profile"]["data"] = data

    return render(request, 'layout/bootstrap.html', {"page":page})


def save(request):
    if request.method == "POST":
        form = InventoryUnitsForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            sweetify.success(request, _('Saved Successfull'), timer=1000)
    
    
    return redirect('inventory.unit.add')


def update(request, id):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Unit", "link":"inventory.unit.add"}
    page["nav_links"]["list"] = { "label":"Unit List", "link":"inventory.unit.list"}
    page["update"] = {}
    page["update"]["type"] = "form"
    page["update"]["action"] = "inventory.unit.update"
    page["update"]["record_id"] = id
    page["update"]["method"] = "post"
    page["update"]["title"] = _("Edit Unit")
    
    instance = InventoryUnits.objects.get(id=id)
    form = InventoryUnitsForm(request.POST or None, instance=instance)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            sweetify.success(request, _('Updated Successfull'), timer=1000)
            return redirect('inventory.unit.update', id = id)
        else:
            sweetify.success(request, _('Action Error'), timer=1000)
    
    
    page["update"]["form"] = form
    return render(request, 'layout/bootstrap.html', {"page":page})


def delete(request, id):
    InventoryUnits.objects.filter(id=id).delete()
    sweetify.success(request, _('Deleted Successfull'), timer=1000)
    return redirect('inventory.unit.list')