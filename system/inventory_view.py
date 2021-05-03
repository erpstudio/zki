from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from .models import Inventory

from django import forms
import django_tables2 as tables
import sweetify


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('name', 'unit', 'category', 'purchase_price', 'sale_price', 'in_stock')
        widgets = {
                'name': forms.TextInput(attrs={'placeholder': _('Name')}),
                # 'category': forms.Select(attrs={'class': 'select2', 'width':'100%'})
        }
    

ACTIONS = '''
   <div class="btn-group"> 
   <a class="btn btn-primary" href="{% url 'inventory.update' record.id %}">Edit</a>
   <a class="btn btn-info" href="{% url 'inventory.show' record.id %}">View</a>
   <a class="btn btn-danger" href="{% url 'inventory.delete' record.id %}">Delete</a>
   </div>
'''

class InventoryTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    class Meta:
        model = Inventory
        fields = ('name', 'unit', 'category', 'purchase_price', 'sale_price', 'in_stock')
        class Meta:
            attrs = {"test": "test"}


page_title = _("Inventory")

def add_page(form=None):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Inventory", "link":"inventory.add"}
    page["nav_links"]["list"] = { "label":"Inventory List", "link":"inventory.list"}
    page["add"] = {}
    page["add"]["type"] = "form"
    page["add"]["action"] = "inventory.save"
    page["add"]["method"] = "post"
    page["add"]["title"] = _("Add Inventory")
    page["add"]["form"] = form
    return page

# Create your views here.
def index(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Inventory", "link":"inventory.add"}
    page["nav_links"]["list"] = { "label":"Inventory List", "link":"inventory.list"}
    return render(request, 'layout/bootstrap.html', {"page":page})


def add(request):
    page = add_page(InventoryForm())
    return render(request, 'layout/bootstrap.html', {"page":page})


def list(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Inventory", "link":"inventory.add"}
    page["nav_links"]["list"] = { "label":"Inventory List", "link":"inventory.list"}
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("Inventory List")
    page["list"]["table"] = InventoryTable(Inventory.objects.all())
    
    return render(request, 'layout/bootstrap.html', {"page":page, "page_title":page_title})

def show(request, id):

    instance = Inventory.objects.get(id=id)

    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Inventory", "link":"inventory.add"}
    page["nav_links"]["list"] = { "label":"Inventory List", "link":"inventory.list"}
    page["profile"] = {}
    page["profile"]["type"] = "profile"
    page["profile"]["title"] = instance.name
    
    data = {}
    data[_("category")] = instance.category.name
    data[_("purchase_price")] = instance.purchase_price
    data[_("sale_price")] = instance.sale_price
    data[_("in_stock")] = instance.in_stock
    
    page["profile"]["data"] = data

    
    return render(request, 'layout/bootstrap.html', {"page":page})


def save(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            sweetify.success(request, _('Saved Successfull'), timer=1000)
            return redirect('inventory.add')

        page = add_page(InventoryForm())
        return render(request, 'layout/bootstrap.html', {"page":page})

    return redirect('inventory.add')
        



def update(request, id):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Inventory", "link":"inventory.add"}
    page["nav_links"]["list"] = { "label":"Inventory List", "link":"inventory.list"}
    page["update"] = {}
    page["update"]["type"] = "form"
    page["update"]["action"] = "inventory.update"
    page["update"]["record_id"] = id
    page["update"]["method"] = "post"
    page["update"]["title"] = _("Edit Inventory")
    
    instance = Inventory.objects.get(id=id)
    form = InventoryForm(request.POST or None, instance=instance)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            sweetify.success(request, _('Updated Successfull'), timer=1000)
            return redirect('inventory.update', id = id)
        else:
            sweetify.success(request, _('Action Error'), timer=1000)
    
    
    page["update"]["form"] = form
    return render(request, 'layout/bootstrap.html', {"page":page})


def delete(request, id):
    Inventory.objects.filter(id=id).delete()
    sweetify.success(request, _('Deleted Successfull'), timer=1000)
    return redirect('inventory.list')