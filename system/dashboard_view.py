from django.shortcuts import render
from django.utils.translation import ugettext as _
import datetime as dt
from django.db.models import Sum


from installment.models import SaleEntry, InstallmentSchedule, ScheduledInstallmentPayment

page_title = "Dashboard"
# Create your views here.
def index(request):
    sch_installment = InstallmentSchedule.objects
    page = {}
    page["page_title"]= page_title
    page["installments_today"] = {}
    page["installments_today"]["type"] = "form"
    page["installments_today"]["template"] = "layout/include/info_color_card.html"
    page["installments_today"]["size"] = "4"
    page["installments_today"]["icon"] = "ion ion-pie-graph"
    page["installments_today"]["color"] = "bg-info"
    page["installments_today"]["more_info"] = "installment.today"
    page["installments_today"]["title"] = _("Today")

    today_pending_inst = sch_installment.filter(scheduledinstallmentpayment=None).filter(scheduled_date=dt.date.today()).count()
    today_total_inst = sch_installment.filter(scheduled_date=dt.date.today()).count()
    today_received_inst = today_total_inst-today_pending_inst
    page["installments_today"]["label"] = "{}: {} | {}: {} |  {}: {}".format(_("Total"),today_total_inst, _("Recieved"), today_received_inst, _("Pending"),today_pending_inst)

    page["installments_overall"] = {}
    page["installments_overall"]["type"] = "form"
    page["installments_overall"]["template"] = "layout/include/info_color_card.html"
    page["installments_overall"]["size"] = "4"
    page["installments_overall"]["icon"] = "ion ion-pie-graph"
    page["installments_overall"]["color"] = "bg-info"
    page["installments_overall"]["more_info"] = "installment.today"
    page["installments_overall"]["title"] = _("Overall")

    overall_pending_inst = sch_installment.filter(scheduledinstallmentpayment=None).count()
    overall_total_inst = sch_installment.count()
    overall_received_inst = overall_total_inst-overall_pending_inst
    page["installments_overall"]["label"] = "{}: {} | {}: {} |  {}: {}".format(_("Total"),overall_total_inst, _("Recieved"), overall_received_inst, _("Pending"),overall_pending_inst)

    page["today_recovery"] = {}
    page["today_recovery"]["type"] = "form"
    page["today_recovery"]["template"] = "layout/include/info_color_card.html"
    page["today_recovery"]["size"] = "4"
    page["today_recovery"]["icon"] = "ion ion-stats-bars"
    page["today_recovery"]["color"] = "bg-success"
    page["today_recovery"]["more_info"] = "installment.today"
    page["today_recovery"]["title"] = _("Today Recovery")

    today_pending_inst_amount = sch_installment.filter(scheduledinstallmentpayment=None).filter(scheduled_date=dt.date.today()).aggregate(Sum('installment_amount')).get('installment_amount__sum', 0)
    if today_pending_inst_amount is None: today_pending_inst_amount = 0
    today_total_inst_amount = sch_installment.filter(scheduled_date=dt.date.today()).aggregate(Sum('installment_amount')).get('installment_amount__sum', 0)
    if today_total_inst_amount is None: today_total_inst_amount = 0

    today_received_inst_amount = today_total_inst_amount-today_pending_inst_amount
    page["today_recovery"]["label"] = "{}: {} | {}: {} |  {}: {}".format(_("Total"),today_total_inst_amount, _("Recieved"), today_received_inst_amount, _("Pending"),today_pending_inst_amount)
    
    page["recovery_by_area"] = {}
    page["recovery_by_area"]["type"] = "form"
    page["recovery_by_area"]["template"] = "layout/include/bar_chart.html"
    page["recovery_by_area"]["size"] = "12"
    page["recovery_by_area"]["icon"] = "ion ion-stats-bars"
    page["recovery_by_area"]["color"] = "bg-success"
    page["recovery_by_area"]["more_info"] = "installment.today"
    page["recovery_by_area"]["title"] = _("Today Reccovery By Area")

    data = {}
    labels = []
    values = []

    group_by_area = sch_installment.values('sale_entry__areazone__name').filter(scheduledinstallmentpayment=None).filter(scheduled_date=dt.date.today()).annotate(Sum('installment_amount'))
    for area in group_by_area:
        labels.append(area["sale_entry__areazone__name"]) 
        values.append(area["installment_amount__sum"])  
    
    data["labels"] = labels
    data["values"] = values
    page["recovery_by_area"]["data"] = data


    return render(request, 'layout/bootstrap.html', {"page":page})