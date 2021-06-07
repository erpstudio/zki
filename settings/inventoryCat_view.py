from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from .models import InventoryCategory

from django import forms
import django_tables2 as tables
import sweetify


class InventoryCategoryForm(forms.ModelForm):
    class Meta:
        model = InventoryCategory
        fields = ('name', 'description')
        widgets = {
                'name': forms.TextInput(attrs={'placeholder': _('Name')}),
                # 'category': forms.Select(attrs={'class': 'select2', 'width':'100%'})
        }
    

ACTIONS = '''
   <div class="btn-group"> 
   <a class="btn btn-primary" href="{% url 'inventory.category.update' record.id %}">Edit</a>
   <a class="btn btn-info" href="{% url 'inventory.category.show' record.id %}">View</a>
   <a class="btn btn-danger" href="{% url 'inventory.category.delete' record.id %}">Delete</a>
   </div>
'''

class InventoryCategoryTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    class Meta:
        model = InventoryCategory
        fields = ('name', 'description')


page_title = _("Inventory Category")


# Create your views here.
def index(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Category", "link":"inventory.category.add"}
    page["nav_links"]["list"] = { "label":"Category List", "link":"inventory.category.list"}
    return render(request, 'layout/bootstrap.html', {"page":page})


def add(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Category", "link":"inventory.category.add"}
    page["nav_links"]["list"] = { "label":"Category List", "link":"inventory.category.list"}
    page["add"] = {}
    page["add"]["type"] = "form"
    page["add"]["action"] = "inventory.category.save"
    page["add"]["method"] = "post"
    page["add"]["title"] = _("Add Category")
    page["add"]["form"] = InventoryCategoryForm()
    
    return render(request, 'layout/bootstrap.html', {"page":page})


def list(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Category", "link":"inventory.category.add"}
    page["nav_links"]["list"] = { "label":"Category List", "link":"inventory.category.list"}
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("Category List")
    page["list"]["table"] = InventoryCategoryTable(InventoryCategory.objects.all())
    
    return render(request, 'layout/bootstrap.html', {"page":page, "page_title":page_title})

def show(request, id):

    instance = InventoryCategory.objects.get(id=id)

    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Category", "link":"inventory.category.add"}
    page["nav_links"]["list"] = { "label":"Category List", "link":"inventory.category.list"}
    page["profile"] = {}
    page["profile"]["type"] = "profile"
    page["profile"]["title"] = instance.name
    page["profile"]["slogan"] = instance.description
    
    data = {}
    page["profile"]["data"] = data

    return render(request, 'layout/bootstrap.html', {"page":page})


def save(request):
    if request.method == "POST":
        form = InventoryCategoryForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            sweetify.success(request, _('Saved Successfull'), timer=1000)
    
    
    return redirect('inventory.category.add')


def update(request, id):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Category", "link":"inventory.category.add"}
    page["nav_links"]["list"] = { "label":"Category List", "link":"inventory.category.list"}
    page["update"] = {}
    page["update"]["type"] = "form"
    page["update"]["action"] = "inventory.category.update"
    page["update"]["record_id"] = id
    page["update"]["method"] = "post"
    page["update"]["title"] = _("Edit Category")
    
    instance = InventoryCategory.objects.get(id=id)
    form = InventoryCategoryForm(request.POST or None, instance=instance)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            sweetify.success(request, _('Updated Successfull'), timer=1000)
            return redirect('inventory.category.update', id = id)
        else:
            sweetify.success(request, _('Action Error'), timer=1000)
    
    
    page["update"]["form"] = form
    return render(request, 'layout/bootstrap.html', {"page":page})


def delete(request, id):
    InventoryCategory.objects.filter(id=id).delete()
    sweetify.success(request, _('Deleted Successfull'), timer=1000)
    return redirect('inventory.category.list')