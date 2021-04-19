from django.shortcuts import render
from django.utils.translation import ugettext as _
from .models import Inventory
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Fieldset, Field, Column, Row
from django.shortcuts import redirect
import sweetify


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('name', 'unit', 'category', 'purchase_price', 'sale_price', 'in_stock')
        widgets = {
                'name': forms.TextInput(attrs={'placeholder': _('Name')}),
                # 'category': forms.Select(attrs={'class': 'select2', 'width':'100%'}),
                # 'unit': forms.Select(attrs={'class': 'select2', 'width':'100%'}),
        }
        # category = widget=forms.Select(attrs={'class': 'select2'})
    

page = {
    "page_title":"Inventory",
        "add_inventory":{
            "type":"form",
            "title":_("Add Inventory"),
            "action":"inventory.save",
            "method":"post"
        }
    }


# Create your views here.
def index(request):
    page["add_inventory"]["form"] = InventoryForm()
    return render(request, 'layout/bootstrap.html', {"page":page})


def show(request):
    context = {}
    cards["add_inventory"]["form"] = InventoryForm()
    context["cards"] = cards
    
    return render(request, 'system/inventory/index.html', context)


def add(request):
    page["add_inventory"]["form"] = InventoryForm()
    return render(request, 'layout/bootstrap.html', {"page":page})

def save(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        print(form)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.save()
            sweetify.success(request, 'Save Successfully', timer=1000)
    else:
        form = Inventory()
    
    
    return redirect('inventory.add')


def update(request):
    context = {}
    cards["add_inventory"]["form"] = InventoryForm()
    context["cards"] = cards
    
    return render(request, 'system/inventory/index.html', context)


def delete(request):
    context = {}
    cards["add_inventory"]["form"] = InventoryForm()
    context["cards"] = cards
    
    return render(request, 'system/inventory/index.html', context)