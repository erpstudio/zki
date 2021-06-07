from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
import datetime as dt

from .models import SaleEntry, InstallmentSchedule, ScheduledInstallmentPayment
from system.models import AreaZone
from django import forms
import django_tables2 as tables
import sweetify

ACTIONS = '''
   <div class="btn-group"> 
   <a class="btn btn-info" href="{% url 'sale.entry.show' record.id %}">View</a>
   </div>
'''


class AreaZoneForm(forms.Form):
    Area = forms.ModelChoiceField(queryset=AreaZone.objects.all().order_by('name'))
    # class Meta:
        # model = AreaZone
        # fields = ('name',)
        # widgets = {
        #         # 'vendor': forms.TextInput(attrs={'placeholder': _('Name')}),
        #         'vendor': forms.Select(attrs={'class': 'select2', 'width':'100%'}),
        #         'inventory': forms.Select(attrs={'class': 'select2', 'width':'100%'})
        # }


class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)

class SaleEntryTable(tables.Table):
    actions = tables.TemplateColumn(ACTIONS)
    customer = tables.Column(footer="Total")
    installment_amount = SummingColumn()
    class Meta:
        model = SaleEntry
        fields = ('customer', 'inventory', 'unit_price', 'quantity', 'total_amount', 'first_installment_date', 'installment_interval_days', 'installment_amount')
        

class InstallmentScheduleTable(tables.Table):
    sale_entry__id = tables.Column(verbose_name=_('Sale ID'))
    pay_installment = tables.TemplateColumn("""
    {% if record.sale_entry.balance == 0 %}
        {% if record.paid == False %}
            <form action="{% url "installment.updateStatustoPaid" %}" method="POST">
            {% csrf_token %}
            <input type="hidden" name="sale_entry" value="{{ record.sale_entry.id }}">
            <button class="btn btn-success" title="Balance is 0 Update Pending Status Installments">Clear Sale Installments</button>
            </form>
            {% else %}
            <strong class="text-success"><i class="fas fa-check"></i></strong>
        {% endif %}
        {% else %}
        {% if record.paid == False %}
            <form class="confirm-form" action="{% url 'installment.payment' record.id %}" method="post">
                {% csrf_token %}
                <div class="input-group input-group-sm mb-3">
                    <input type="number" class="form-control" style="width:80px" name="pay_amount" value="{{ record.installment_amount }}" />
                    <div class="input-group-append">
                    <button class="btn btn-info" type="submit">Recieve</button>
                    </div>
                </div>
            </form>
            {% else %}
                <strong class="text-success">Paid</strong>
            {% endif %}
    {% endif %}
    """, verbose_name=_('Installment Payment'))

    # sale_entry__customer = tables.Column(footer="Total")
    installment_amount = SummingColumn()
    class Meta:
        model = InstallmentSchedule
        fields = ('sale_entry.customer', 'sale_entry.inventory', 'sale_entry.areazone', 'scheduled_date', 'installment_amount', 'sale_entry__balance')
        

page_title = _("Installments")

def today(request):
    page = {}
    page["page_title"]= page_title

    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Sale Entry"), "link":"sale.entry.add"}
    page["nav_links"]["list"] = { "label":_("Sale List"), "link":"sale.entry.list"}
    page["area"] = {}
    page["area"]["type"] = "form"
    page["area"]["title"] = _("Filter By Area")
    page["area"]["form"] = AreaZoneForm()
    page["area"]["action"] = "installment.today"
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("Today Installments")

    if request.method == "POST":
        form = AreaZoneForm(request.POST)
        form.is_valid()
        form = form.cleaned_data
        areazone = form["Area"]
        data = InstallmentSchedule.objects.filter(paid=False).filter(scheduled_date=dt.date.today()).filter(sale_entry__areazone = areazone)
    else:
        data = InstallmentSchedule.objects.filter(paid=False).filter(scheduled_date=dt.date.today())
    
    page["list"]["table"] = InstallmentScheduleTable(data)
    
    return render(request, 'layout/bootstrap.html', {"page":page, "page_title":page_title})


def pending(request):
    page = {}
    page["page_title"]= page_title

    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Sale Entry"), "link":"sale.entry.add"}
    page["nav_links"]["list"] = { "label":_("Sale List"), "link":"sale.entry.list"}
    page["area"] = {}
    page["area"]["type"] = "form"
    page["area"]["title"] = _("Filter By Area")
    page["area"]["form"] = AreaZoneForm()
    page["area"]["action"] = "installment.pending"
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("Pending Installments")

    if request.method == "POST":
        form = AreaZoneForm(request.POST)
        form.is_valid()
        form = form.cleaned_data
        areazone = form["Area"]
        data = InstallmentSchedule.objects.filter(paid=False).filter(scheduled_date__lt=dt.date.today()).filter(sale_entry__areazone = areazone)
    else:
        data = InstallmentSchedule.objects.filter(paid=False).filter(scheduled_date__lt=dt.date.today())
    
    page["list"]["table"] = InstallmentScheduleTable(data)
    
    return render(request, 'layout/bootstrap.html', {"page":page, "page_title":page_title})

def payment(request,id):
    if request.method == "POST":
        form = request.POST
        paid_amount = form.get('pay_amount')
        sch_installment = InstallmentSchedule.objects.get(id=id)
        sch_installment_p_save = ScheduledInstallmentPayment.objects.create(
            scheduled_installment = sch_installment,
            paid_amount = paid_amount
        )
        sch_installment_p_save.save()
        # print(sch_installment)
    
    return redirect(request.META.get('HTTP_REFERER'))


def show(request, id):

    instance = SaleEntry.objects.get(id=id)

    page = {}
    page["page_title"]= page_title
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Add Entry"), "link":"sale.entry.add"}
    page["nav_links"]["list"] = { "label":_("Entry List"), "link":"sale.entry.list"}
    page["profile"] = {}
    page["profile"]["type"] = "profile"
    id = instance.id
    page["profile"]["title"] = "{}: {}".format(_("Transaction#"), id)
    
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

    

def updateStatustoPaid(request):
    if request.method == "POST":
        
        form = request.POST
        sale_entry = form["sale_entry"]
        print(sale_entry)
        sch_ins = InstallmentSchedule.objects.filter(sale_entry=sale_entry).update(paid=True)
        sweetify.success(request, _('Successfull Done'), timer=2000)
        return redirect(request.META.get('HTTP_REFERER'))
        
        
    sweetify.warning(request, _('Only Post Method Allowed'), timer=2000)
    return redirect(request.META.get('HTTP_REFERER'))

    

