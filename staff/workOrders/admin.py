from django.contrib import admin
from workOrders.models import WorkOrder, Order

import pandas as pd
import string
from datetime import datetime
#from decimal import *

def getAcronym(filename):
    return filename[27:33]

def removeDummyProyects(report):
    return report[report.Project.str.contains('^X')==False]


def getReport(fileName):
    report = pd.read_csv(fileName, sep=';', names=['Date','Hours','Project','Phase','SubPhase','Task','OnCall','CallIn'])
    report['staffId']=getAcronym(fileName.name)
    report['Hours'] = report['Hours'].apply(lambda x: float(string.replace(x,',','.')))
    report['Date'] = [datetime.strptime(x, '%d/%m/%Y') for x in report['Date']]
    report['Period'] = [str(_date.year)+'-'+str(_date.month)+'-01' for _date in report['Date']]
    return removeDummyProyects(report)


def deleteOldOrders(workorder):
	for order in Order.objects.filter(workOrder__id=workorder.id):
		order.delete()

def processWorkOrder(modeladmin, request, queryset):
	for workorder in queryset:
		deleteOldOrders(workorder)
		workOrderProcess = getReport(workorder.woFile).groupby(['staffId','Project','Period'], as_index=False).sum()
        totHours=workOrderProcess['Hours'].sum()
        bill = float(workorder.total_No_Taxes)
        workOrderProcess['Percentage'] = workOrderProcess['Hours']/totHours
        workOrderProcess['Amount'] = workOrderProcess['Percentage']*bill
        for orderProcess in workOrderProcess.iterrows():
        	#print orderProcess[1]
        	order = Order(workOrder=workorder, staffId=orderProcess[1]['staffId'], 
        					project = orderProcess[1]['Project'],
        					woDate=orderProcess[1]['Period'], hours = orderProcess[1]['Hours'], 
        					perctHours = orderProcess[1]['Percentage'], total = orderProcess[1]['Amount'])
        	order.save()
        workorder.processed = True
        workorder.staffId = getAcronym(workorder.woFile.name)
        workorder.save()

processWorkOrder.short_description = "Process selected workorders"

class OrderInline(admin.TabularInline):
	model = Order
	extra = 0
	urls = []
	def get_model_perms(self, request):
		return {}
	fieldsets = [
		(None, {'fields': ['staffId', 'project', 'woDate', 'hours', 'total']})
	]

class WorkOrderAdmin(admin.ModelAdmin):
	readonly_fields = ['processed', 'staffId']
	fieldsets = [
		(None, {'fields': ['staffId', 'processed', 'woDate', 'total_No_Taxes', 'woFile']}),
	]
	#fields = ['processed','staffId', 'woDate', 'total_No_Taxes', 'woFile']
	list_display = ('staffId', 'processed','woDate', 'total_No_Taxes', 'woFile')
	inlines = [OrderInline]
	actions = [processWorkOrder]



# Register your models here.
admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(Order, OrderInline)