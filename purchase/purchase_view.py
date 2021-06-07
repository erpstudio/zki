from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from .models import PurchaseEntry

from django import forms
import django_tables2 as tables
import sweetify


class PurchaseEntryForm(forms.ModelForm):
    class Meta:
        model = PurchaseEntry
        fields = ('vendor', 'inventory', 'unit_price', 'quantity', 'total_amount')
        widgets = {
                # 'vendor': forms.TextInput(attrs={'placeholder': _('Name')}),
                'vendor': forms.Select(attrs={'class': 'select2', 'width':'100%'}),
                'inventory': forms.Select(attrs={'class': 'select2', 'width':'100%'})
        }


ACTIONS = '''
   <div class="btn-group"> 
   <a class="btn btn-info" href="{% url 'purchase.entry.show' record.id %}">View</a>
   </div>
'''


class PurchaseEntryTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    class Meta:
        model = PurchaseEntry
        fields = ('id', 'vendor', 'inventory', 'unit_price', 'quantity', 'total_amount')
        

page_title = _("Purchase Entry")

def add_page(form=None):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Add Entry"), "link":"purchase.entry.add"}
    page["nav_links"]["list"] = { "label":_("Entry List"), "link":"purchase.entry.list"}
    page["add"] = {}
    page["add"]["type"] = "form"
    page["add"]["template"] = "layout/include/purchase_form.html"
    page["add"]["action"] = "purchase.entry.save"
    page["add"]["method"] = "post"
    page["add"]["title"] = _("Purchase")
    page["add"]["form"] = form
    
    return page

def add(request):
    page = add_page(form=PurchaseEntryForm())
    return render(request, 'layout/bootstrap.html', {"page":page})


def list(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Add Entry"), "link":"purchase.entry.add"}
    page["nav_links"]["list"] = { "label":_("Entry List"), "link":"purchase.entry.list"}
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("Entry List")
    page["list"]["table"] = PurchaseEntryTable(PurchaseEntry.objects.all())
    
    return render(request, 'layout/bootstrap.html', {"page":page, "page_title":page_title})

def show(request, id):

    instance = PurchaseEntry.objects.get(id=id)

    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Add Entry"), "link":"purchase.entry.add"}
    page["nav_links"]["list"] = { "label":_("Entry List"), "link":"purchase.entry.list"}
    page["profile"] = {}
    page["profile"]["type"] = "profile"
    id = instance.id
    page["profile"]["title"] = "{}: {}".format(_("Transaction#"), id)
    
    data = {}
    data[_("vendor")] = instance.vendor
    data[_("inventory")] = instance.inventory
    data[_("unit_price")] = instance.unit_price
    data[_("quantity")] = instance.quantity
    data[_("total_amount")] = instance.total_amount
    
    page["profile"]["data"] = data

    
    return render(request, 'layout/bootstrap.html', {"page":page})


def save(request):
    if request.method == "POST":
        form = PurchaseEntryForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            sweetify.success(request, _('Saved Successfull'), timer=1000)
            return redirect('purchase.entry.add')
        
        page = add_page(form=form)
        return render(request, 'layout/bootstrap.html', {"page":page})

    
    return redirect('purchase.entry.add')

