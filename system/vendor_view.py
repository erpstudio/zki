from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from .models import Vendor

from django import forms
import django_tables2 as tables
import sweetify


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('name', 'father_name', 'category', 'mobile', 'cnic', 'address')
        widgets = {
                'name': forms.TextInput(attrs={'placeholder': _('Name')}),
                # 'category': forms.Select(attrs={'class': 'select2', 'width':'100%'})
        }
    

ACTIONS = '''
   <div class="btn-group"> 
   <a class="btn btn-primary" href="{% url 'vendor.update' record.id %}">Edit</a>
   <a class="btn btn-info" href="{% url 'vendor.show' record.id %}">View</a>
   <a class="btn btn-danger" href="{% url 'vendor.delete' record.id %}">Delete</a>
   </div>
'''

class VendorTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    class Meta:
        model = Vendor
        class Meta:
            attrs = {"test": "test"}


page_title = _("Vendor")


# Create your views here.
def index(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Vendor", "link":"vendor.add"}
    page["nav_links"]["list"] = { "label":"Vendor List", "link":"vendor.list"}
    return render(request, 'layout/bootstrap.html', {"page":page})


def add(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Vendor", "link":"vendor.add"}
    page["nav_links"]["list"] = { "label":"Vendor List", "link":"vendor.list"}
    page["add"] = {}
    page["add"]["type"] = "form"
    page["add"]["action"] = "vendor.save"
    page["add"]["method"] = "post"
    page["add"]["title"] = _("Add Vendor")
    page["add"]["form"] = VendorForm()
    
    return render(request, 'layout/bootstrap.html', {"page":page})


def list(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Vendor", "link":"vendor.add"}
    page["nav_links"]["list"] = { "label":"Vendor List", "link":"vendor.list"}
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("Vendor List")
    page["list"]["table"] = VendorTable(Vendor.objects.all())
    
    return render(request, 'layout/bootstrap.html', {"page":page, "page_title":page_title})

def show(request, id):

    instance = Vendor.objects.get(id=id)

    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Vendor", "link":"vendor.add"}
    page["nav_links"]["list"] = { "label":"Vendor List", "link":"vendor.list"}
    page["profile"] = {}
    page["profile"]["type"] = "profile"
    page["profile"]["title"] = instance.name
    page["profile"]["slogan"] = instance.father_name
    
    data = {}
    data[_("category")] = instance.category.name
    data[_("address")] = instance.address
    data[_("cnic")] = instance.cnic
    data[_("mobile")] = instance.mobile
    data[_("balance")] = instance.balance
    
    page["profile"]["data"] = data

    
    return render(request, 'layout/bootstrap.html', {"page":page})


def save(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            sweetify.success(request, _('Saved Successfull'), timer=1000)
    
    
    return redirect('vendor.add')


def update(request, id):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Vendor", "link":"vendor.add"}
    page["nav_links"]["list"] = { "label":"Vendor List", "link":"vendor.list"}
    page["update"] = {}
    page["update"]["type"] = "form"
    page["update"]["action"] = "vendor.update"
    page["update"]["record_id"] = id
    page["update"]["method"] = "post"
    page["update"]["title"] = _("Edit Vendor")
    
    instance = Vendor.objects.get(id=id)
    form = VendorForm(request.POST or None, instance=instance)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            sweetify.success(request, _('Updated Successfull'), timer=1000)
            return redirect('vendor.update', id = id)
        else:
            sweetify.success(request, _('Action Error'), timer=1000)
    
    
    page["update"]["form"] = form
    return render(request, 'layout/bootstrap.html', {"page":page})


def delete(request, id):
    Vendor.objects.filter(id=id).delete()
    sweetify.success(request, _('Deleted Successfull'), timer=1000)
    return redirect('vendor.list')