from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from .models import SaleEntry

from django import forms
import django_tables2 as tables
import sweetify


class SaleEntryForm(forms.ModelForm):
    class Meta:
        model = SaleEntry
        fields = ('customer', 'inventory', 'unit_price', 'quantity', 'total_amount', 'installment_started', 'installment_interval_days', 'installment_amount')
        widgets = {
                # 'vendor': forms.TextInput(attrs={'placeholder': _('Name')}),
                'vendor': forms.Select(attrs={'class': 'select2', 'width':'100%'}),
                'inventory': forms.Select(attrs={'class': 'select2', 'width':'100%'})
        }


ACTIONS = '''
   <div class="btn-group"> 
   <a class="btn btn-info" href="{% url 'sale.entry.show' record.id %}">View</a>
   </div>
'''


class SaleEntryTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    class Meta:
        model = SaleEntry
        fields = ('customer', 'inventory', 'unit_price', 'quantity', 'total_amount', 'installment_started', 'installment_interval_days', 'installment_amount')
        

page_title = _("Sale Entry")

def add_page(form=None):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Add Entry"), "link":"sale.entry.add"}
    page["nav_links"]["list"] = { "label":_("Entry List"), "link":"sale.entry.list"}
    page["add"] = {}
    page["add"]["type"] = "form"
    page["add"]["template"] = "layout/include/purchase_form.html"
    page["add"]["action"] = "sale.entry.save"
    page["add"]["method"] = "post"
    page["add"]["title"] = _("Sale")
    page["add"]["form"] = form
    page["add1"] = {}
    page["add1"]["type"] = "form"
    page["add1"]["template"] = "layout/include/purchase_form.html"
    page["add1"]["action"] = "sale.entry.save"
    page["add1"]["method"] = "post"
    page["add1"]["title"] = _("Test Card")
    
    return page

def add(request):
    
    page = add_page(form=SaleEntryForm())
    
    return render(request, 'layout/bootstrap.html', {"page":page})


def list(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Add Entry"), "link":"sale.entry.add"}
    page["nav_links"]["list"] = { "label":_("Entry List"), "link":"sale.entry.list"}
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("Entry List")
    page["list"]["table"] = SaleEntryTable(SaleEntry.objects.all())
    
    return render(request, 'layout/bootstrap.html', {"page":page, "page_title":page_title})

def show(request, id):

    instance = SaleEntry.objects.get(id=id)

    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Add Entry"), "link":"sale.entry.add"}
    page["nav_links"]["list"] = { "label":_("Entry List"), "link":"sale.entry.list"}
    page["profile"] = {}
    page["profile"]["type"] = "profile"
    page["profile"]["title"] = _("Transaction#: {}").format(instance.id)
    
    data = {}
    data[_("vendor")] = instance.customer
    data[_("inventory")] = instance.inventory
    data[_("installment_interval_days")] = instance.installment_interval_days
    data[_("installment_amount")] = instance.installment_amount
    data[_("unit_price")] = instance.unit_price
    data[_("quantity")] = instance.quantity
    data[_("total_amount")] = instance.total_amount
    
    page["profile"]["data"] = data

    
    return render(request, 'layout/bootstrap.html', {"page":page})


def save(request):
    if request.method == "POST":
        form = SaleEntryForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            sweetify.success(request, _('Saved Successfull'), timer=1000)
            return redirect('sale.entry.add')
        
        page = add_page(form=form)
        return render(request, 'layout/bootstrap.html', {"page":page})
        
    return redirect('sale.entry.add')

    

