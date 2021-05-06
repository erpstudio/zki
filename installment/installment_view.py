from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
import datetime as dt

from .models import SaleEntry, InstallmentSchedule

from django import forms
import django_tables2 as tables
import sweetify

ACTIONS = '''
   <div class="btn-group"> 
   <a class="btn btn-info" href="{% url 'sale.entry.show' record.id %}">View</a>
   </div>
'''


class SaleEntryTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    class Meta:
        model = SaleEntry
        fields = ('customer', 'inventory', 'unit_price', 'quantity', 'total_amount', 'first_installment_date', 'installment_interval_days', 'installment_amount')
        

class InstallmentScheduleTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    class Meta:
        model = InstallmentSchedule
        fields = ('sale_entry.customer', 'sale_entry.inventory', 'sale_entry.areazone', 'scheduled_date', 'installment_amount')
        

page_title = _("Installments")

def today(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Sale Entry"), "link":"sale.entry.add"}
    page["nav_links"]["list"] = { "label":_("Sale List"), "link":"sale.entry.list"}
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("Today Installments")

    data = InstallmentSchedule.objects.filter()
    print(dt.date.today())
    page["list"]["table"] = InstallmentScheduleTable(data)
    
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

    

