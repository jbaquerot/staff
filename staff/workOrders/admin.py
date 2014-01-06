from django.contrib import admin
from workOrders.models import WorkOrder, Order, Staff


class StaffAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['staffId','name','surname','company', 'start_Date', 'end_Date', 'daily_Rate']})
    ]
    list_display = ('staffId', 'name','surname',  'company', 'start_Date', 'end_Date', 'daily_Rate')

    list_filter = ['company', 'end_Date', 'staffId']



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

    def process(self, request, queryset):
        """ 
        """
        for workorder in queryset:
            if (workorder.total_No_Taxes == None) :
                break
            workorder.deleteAllOrders()
            workOrderProcess = workorder.getReport().groupby(['staffId','Project','Period'], as_index=False).sum()
            totHours = workOrderProcess['Hours'].sum()
            bill = float(workorder.total_No_Taxes)
            workOrderProcess['Percentage'] = workOrderProcess['Hours']/totHours
            workOrderProcess['Amount'] = workOrderProcess['Percentage']*bill

            for orderProcess in workOrderProcess.iterrows():
                order = Order(workOrder=workorder, staffId=orderProcess[1]['staffId'], 
                                project = orderProcess[1]['Project'],
                                woDate=orderProcess[1]['Period'], hours = orderProcess[1]['Hours'], 
                                perctHours = orderProcess[1]['Percentage'], total = orderProcess[1]['Amount'])
                order.save()
            
            workorder.state = WorkOrder.PROCESSED
            #workorder.staffId = Staff.object.get(getAcronym(workorder.woFile.name))
            workorder.save(force_update=True)
            #workorder.save(force_update=True, update_fields=['state','staffId','staffId_id'])
            print "WorkOrder PROCESSED"

    process.short_description = "Process selected workorders"

    def delete(self, request, queryset):
        for workorder in queryset:
            workorder.delete()

    delete.short_description = 'Delete selected workorders'


    readonly_fields = ['staffId','woDate','getStaffName']

    fieldsets = [
        ('Staff', {'fields': ['staffId','getStaffName']}),
        (None, {'fields': ['state', 'woDate', 'total_No_Taxes', 'woFile']}),
        
    ]

    list_display = ('getStaffName','staffId', 'state','woDate', 'total_No_Taxes', 'woFile')

    inlines = [OrderInline]

    actions = [process, delete]

    list_filter = ['state', 'woDate', 'staffId']



admin.site.disable_action('delete_selected')
# Register your models here.
admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(Order, OrderInline)
admin.site.register(Staff, StaffAdmin)