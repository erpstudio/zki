from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from .models import SaleEntry

from django import forms
from django.core.exceptions import ValidationError
import django_tables2 as tables
import sweetify


class SaleEntryForm(forms.ModelForm):
    class Meta:
        model = SaleEntry
        fields = ('customer', 'inventory', 'areazone', 'unit_price', 'quantity', 'total_amount', 'first_installment_date', 'installment_cycle', 'installment_amount', 'no_of_installments')
        widgets = {
                # 'vendor': forms.TextInput(attrs={'placeholder': _('Name')}),
                'vendor': forms.Select(attrs={'class': 'select2', 'width':'100%'}),
                'inventory': forms.Select(attrs={'class': 'select2', 'width':'100%'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        total_amount = cleaned_data.get("total_amount")
        installment_amount = cleaned_data.get("installment_amount")

        if installment_amount > total_amount:
            msg = _("Installment Amount can't be greater then Total Amount")
            self.add_error('installment_amount', msg)



ACTIONS = '''
   <div class="btn-group d-print-none"> 
   <a class="btn btn-info" href="{% url 'sale.entry.show' record.id %}">View</a>
   </div>
'''


class SaleEntryTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    class Meta:
        model = SaleEntry
        fields = ('id', 'customer', 'inventory', 'areazone', 'unit_price', 'quantity', 'total_amount', 'balance')
        

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
    page["list"]["title"] = _("Sale Entry List")
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
    data[_("installment_cycle")] = instance.installment_cycle
    data[_("installment_amount")] = instance.installment_amount
    data[_("unit_price")] = instance.unit_price
    data[_("quantity")] = instance.quantity
    data[_("total_amount")] = instance.total_amount
    data[_("balance")] = instance.balance
    
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

    

