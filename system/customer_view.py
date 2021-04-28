from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from .models import Customer

from django import forms
import django_tables2 as tables
import sweetify


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'father_name', 'mobile', 'cnic', 'address', 'occupation')
        widgets = {
                'name': forms.TextInput(attrs={'placeholder': _('Name')}),
                # 'category': forms.Select(attrs={'class': 'select2', 'width':'100%'})
        }
    

ACTIONS = '''
   <div class="btn-group"> 
   <a class="btn btn-primary" href="{% url 'customer.update' record.id %}">Edit</a>
   <a class="btn btn-info" href="{% url 'customer.show' record.id %}">View</a>
   <a class="btn btn-danger" href="{% url 'customer.delete' record.id %}">Delete</a>
   </div>
'''

class CustomerTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    class Meta:
        model = Customer
        fields = ('name', 'father_name', 'mobile', 'cnic', 'address', 'occupation')
        class Meta:
            attrs = {"test": "test"}


page_title = _("Customer")


# Create your views here.
def index(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Add Customer"), "link":"customer.add"}
    page["nav_links"]["list"] = { "label":_("Customer List"), "link":"customer.list"}
    return render(request, 'layout/bootstrap.html', {"page":page})


def add(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Add Customer"), "link":"customer.add"}
    page["nav_links"]["list"] = { "label":_("Customer List"), "link":"customer.list"}
    page["add"] = {}
    page["add"]["type"] = "form"
    page["add"]["action"] = "customer.save"
    page["add"]["method"] = "post"
    page["add"]["title"] = _("Add Customer")
    page["add"]["form"] = CustomerForm()
    page["action_links"] = {}
    page["action_links"]["grantor"] = { "label":_("Save And Add Grantor"), "link":"customer.list"}
    
    return render(request, 'layout/bootstrap.html', {"page":page})


def list(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Add Customer"), "link":"customer.add"}
    page["nav_links"]["list"] = { "label":_("Customer List"), "link":"customer.list"}
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("Customer List")
    page["list"]["table"] = CustomerTable(Customer.objects.all())
    
    return render(request, 'layout/bootstrap.html', {"page":page, "page_title":page_title})

def show(request, id):

    instance = Customer.objects.get(id=id)

    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Add Customer"), "link":"customer.add"}
    page["nav_links"]["list"] = { "label":_("Customer List"), "link":"customer.list"}
    page["profile"] = {}
    page["profile"]["type"] = "profile"
    page["profile"]["title"] = instance.name
    
    data = {}
    data[_("mobile")] = instance.mobile
    data[_("cnic")] = instance.cnic
    data[_("address")] = instance.address
    
    page["profile"]["data"] = data

    
    return render(request, 'layout/bootstrap.html', {"page":page})


def save(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            sweetify.success(request, _('Saved Successfull'), timer=1000)
    
    
    return redirect('customer.add')


def update(request, id):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Add Customer"), "link":"customer.add"}
    page["nav_links"]["list"] = { "label":_("Customer List"), "link":"customer.list"}
    page["update"] = {}
    page["update"]["type"] = "form"
    page["update"]["action"] = "customer.update"
    page["update"]["record_id"] = id
    page["update"]["method"] = "post"
    page["update"]["title"] = _("Edit Customer")
    
    instance = Customer.objects.get(id=id)
    form = CustomerForm(request.POST or None, instance=instance)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            sweetify.success(request, _('Updated Successfull'), timer=1000)
            return redirect('customer.update', id = id)
        else:
            sweetify.success(request, _('Action Error'), timer=1000)
    
    
    page["update"]["form"] = form
    return render(request, 'layout/bootstrap.html', {"page":page})


def delete(request, id):
    Customer.objects.filter(id=id).delete()
    sweetify.success(request, _('Deleted Successfull'), timer=1000)
    return redirect('customer.list')