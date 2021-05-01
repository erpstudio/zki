from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from .models import Employee

from django import forms
import django_tables2 as tables
import sweetify


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'father_name', 'category', 'mobile', 'cnic', 'address')
        widgets = {
                'name': forms.TextInput(attrs={'placeholder': _('Name')}),
                # 'category': forms.Select(attrs={'class': 'select2', 'width':'100%'})
        }
    

ACTIONS = '''
   <div class="btn-group"> 
   <a class="btn btn-primary" href="{% url 'employee.update' record.id %}">Edit</a>
   <a class="btn btn-info" href="{% url 'employee.show' record.id %}">View</a>
   <a class="btn btn-danger" href="{% url 'employee.delete' record.id %}">Delete</a>
   </div>
'''

class EmployeeTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    class Meta:
        model = Employee
        fields = ('name', 'father_name', 'category', 'mobile', 'cnic', 'address')
        class Meta:
            attrs = {"test": "test"}


page_title = _("Employee")


# Create your views here.
def index(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Employee", "link":"employee.add"}
    page["nav_links"]["list"] = { "label":"Employee List", "link":"employee.list"}
    return render(request, 'layout/bootstrap.html', {"page":page})


def add(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Employee", "link":"employee.add"}
    page["nav_links"]["list"] = { "label":"Employee List", "link":"employee.list"}
    page["add"] = {}
    page["add"]["type"] = "form"
    page["add"]["action"] = "employee.save"
    page["add"]["method"] = "post"
    page["add"]["title"] = _("Add Employee")
    page["add"]["form"] = EmployeeForm()
    
    return render(request, 'layout/bootstrap.html', {"page":page})


def list(request):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Employee", "link":"employee.add"}
    page["nav_links"]["list"] = { "label":"Employee List", "link":"employee.list"}
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("Employee List")
    page["list"]["table"] = EmployeeTable(Employee.objects.all())
    
    return render(request, 'layout/bootstrap.html', {"page":page, "page_title":page_title})

def show(request, id):

    instance = Employee.objects.get(id=id)

    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Employee", "link":"employee.add"}
    page["nav_links"]["list"] = { "label":"Employee List", "link":"employee.list"}
    page["profile"] = {}
    page["profile"]["type"] = "profile"
    page["profile"]["title"] = instance.name
    
    data = {}
    data[_("category")] = instance.category.name
    data[_("mobile")] = instance.mobile
    data[_("cnic")] = instance.cnic
    data[_("address")] = instance.address
    data[_("salary")] = instance.salary
    
    page["profile"]["data"] = data

    
    return render(request, 'layout/bootstrap.html', {"page":page})


def save(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            sweetify.success(request, _('Saved Successfull'), timer=1000)
    
    
    return redirect('employee.add')


def update(request, id):
    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":"Add Employee", "link":"employee.add"}
    page["nav_links"]["list"] = { "label":"Employee List", "link":"employee.list"}
    page["update"] = {}
    page["update"]["type"] = "form"
    page["update"]["action"] = "employee.update"
    page["update"]["record_id"] = id
    page["update"]["method"] = "post"
    page["update"]["title"] = _("Edit Employee")
    
    instance = Employee.objects.get(id=id)
    form = EmployeeForm(request.POST or None, instance=instance)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            sweetify.success(request, _('Updated Successfull'), timer=1000)
            return redirect('employee.update', id = id)
        else:
            sweetify.success(request, _('Action Error'), timer=1000)
    
    
    page["update"]["form"] = form
    return render(request, 'layout/bootstrap.html', {"page":page})


def delete(request, id):
    Employee.objects.filter(id=id).delete()
    sweetify.success(request, _('Deleted Successfull'), timer=1000)
    return redirect('employee.list')