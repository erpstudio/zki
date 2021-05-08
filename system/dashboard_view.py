from django.shortcuts import render
from django.utils.translation import ugettext as _
import datetime as dt

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
    page["installments_today"]["more_info"] = "installment.today"
    page["installments_today"]["action"] = "employee.save"
    page["installments_today"]["method"] = "post"
    today_pending_inst = sch_installment.filter(scheduledinstallmentpayment=None).filter(scheduled_date=dt.date.today()).count()
    today_total_inst = sch_installment.filter(scheduled_date=dt.date.today()).count()
    today_received_inst = today_total_inst-today_pending_inst

    page["installments_today"]["label"] = "{}: {} | {}: {} |  {}: {}".format(_("Total"),today_total_inst, _("Recieved"), today_received_inst, _("Pending"),today_pending_inst)
    page["installments_today"]["title"] = _("Today")

    page["installments_overall"] = {}
    page["installments_overall"]["type"] = "form"
    page["installments_overall"]["template"] = "layout/include/info_color_card.html"
    page["installments_overall"]["size"] = "4"
    page["installments_overall"]["icon"] = "ion ion-pie-graph"
    page["installments_overall"]["more_info"] = "installment.today"
    page["installments_overall"]["action"] = "employee.save"
    page["installments_overall"]["method"] = "post"

    overall_pending_inst = sch_installment.filter(scheduledinstallmentpayment=None).count()
    overall_total_inst = sch_installment.count()
    overall_received_inst = overall_total_inst-overall_pending_inst
    page["installments_overall"]["label"] = "{}: {} | {}: {} |  {}: {}".format(_("Total"),overall_total_inst, _("Recieved"), overall_received_inst, _("Pending"),overall_pending_inst)
    page["installments_overall"]["title"] = _("Overall")
    

    return render(request, 'layout/bootstrap.html', {"page":page})