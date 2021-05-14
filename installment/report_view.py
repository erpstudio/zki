from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
import datetime as dt
from django.db.models import Sum

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


class FilterForm(forms.Form):
    from_date = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}), label=_("From Date"))
    to_date = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}), label=_("To Date"))
    report_type = forms.ChoiceField(choices = (
        ("1", _("Recieved")),
        ("0", _("Pending")),
    ), label=_("Report Type"))

class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)

class InstallmentScheduleTable(tables.Table):
    sale_entry__areazone__name = tables.Column(footer="Total", verbose_name="Area")
    installment_amount__sum = SummingColumn(verbose_name="Amount")
    class Meta:
        model = InstallmentSchedule
        fields = ('sale_entry__areazone__name', 'installment_amount__sum')
        

page_title = _("Installments")

def index(request):
    page = {}
    page["page_title"]= page_title
    list_title = _("Report")
    page["nav_links"] = {}
    page["nav_links"]["add"] = { "label":_("Sale Entry"), "link":"sale.entry.add"}
    page["nav_links"]["list"] = { "label":_("Sale List"), "link":"sale.entry.list"}
    page["filter"] = {}
    page["filter"]["type"] = "form"
    page["filter"]["title"] = _("Filter")
    page["filter"]["form"] = FilterForm()
    page["filter"]["action"] = "installment.report.index"
    page["list"] = {}
    page["list"]["type"] = "table"
    page["list"]["title"] = _("Area Report")
    data = []
    if request.method == "POST":
        form = FilterForm(request.POST)
        form.is_valid()
        form = form.cleaned_data
        paid = form["report_type"]
        paid = bool(int(paid))
        from_date = form["from_date"]
        to_date = form["to_date"]
        report_type = _("Report Recieved") if paid  else _("Pending")
        list_title = "{} : {} to {}".format(report_type, from_date, to_date)
        # data = InstallmentSchedule.objects.filter(paid=False).filter(scheduled_date=dt.date.today()).filter(sale_entry__areazone = type)
        data = InstallmentSchedule.objects.values('sale_entry__areazone__name').filter(paid=paid).filter(scheduled_date__gte=from_date).filter(scheduled_date__lte=to_date).annotate(Sum('installment_amount'))
    
    page["list"]["title"] = list_title
    table = InstallmentScheduleTable(data)
    page["list"]["table"] = table
    return render(request, 'layout/bootstrap.html', {"page":page, "page_title":page_title})

