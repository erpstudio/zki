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


page_title = _("Purchase Entry")

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
    page["add"]["form"] = PurchaseEntryForm()
    
    return render(request, 'layout/bootstrap.html', {"page":page})
