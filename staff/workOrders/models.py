from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
import string
from datetime import datetime

# Create your models here.

class Staff(models.Model):
    staffId = models.CharField(max_length=6)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    company = models.CharField(max_length=20)
    start_Date = models.DateField(auto_now=False)
    end_Date = models.DateField(auto_now=False, null=True, blank=True)
    daily_Rate = models.FloatField()
    
    def __unicode__(self):
        return self.staffId

class WorkOrder(models.Model):
    CREATED = 'CR'
    PROCESSED = 'PR'
    DONE = 'DN'
    STATES = (
            (CREATED, 'Created'),
            (PROCESSED, 'Processed'),
            (DONE, 'Done'),
        )
    state = models.CharField(max_length=2, default=CREATED, choices = STATES)
    staffId = models.ForeignKey(Staff)
    woDate = models.DateField(auto_now=True)
    total_No_Taxes = models.FloatField(blank = True, null=True)
    woFile = models.FileField(upload_to='documents/%Y/%m/%d')

    def __unicode__(self):
        return str(self.staffId) + ':' + str(self.woDate)

    def deleteAllOrders(self):
        for order in Order.objects.filter(workOrder__id=self.id):
            order.delete()
    def getAcronym(self):
        return self.woFile.name[6:12]

    def getStaffName(self):
        return self.staffId.name+' '+self.staffId.surname
    
    getStaffName.admin_order_field = 'staffId'
    getStaffName.short_description = 'Staff Complete Name'
    getStaffName.boolean = False

    def removeDummyProyects(self,report):
        return report[report.Project.str.contains('^X')==False]

    def getReport(self):
        report = pd.read_csv(self.woFile, sep=';', names=['Date','Hours','Project','Phase','SubPhase','Task','OnCall','CallIn'])
        report['staffId']=self.staffId.staffId
        report['Hours'] = report['Hours'].apply(lambda x: float(string.replace(x,',','.')))
        report['Date'] = [datetime.strptime(x, '%d/%m/%Y') for x in report['Date']]
        report['Period'] = [str(_date.year)+'-'+str(_date.month)+'-01' for _date in report['Date']]
        return self.removeDummyProyects(report)

    def save(self, *args, **kwargs):
        print "Saving WorkOrder"
        print "getAcronym:"+self.getAcronym()
        try:
            self.staffId = Staff.objects.get(staffId=self.getAcronym())
        except ObjectDoesNotExist:
            print "stafId:"+str(self.getAcronym())+" doesn't exist"
        super(WorkOrder, self).save(*args, **kwargs)
        print "saved"


class Order(models.Model):
    workOrder = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    staffId = models.CharField(max_length=6)
    project = models.CharField(max_length=30)
    woDate = models.DateField()
    hours = models.FloatField()
    perctHours = models.FloatField()
    total = models.FloatField()

    #def __unicode__(self):
    #   return self.staffId + ':'+ self.project + ':' +str(self.woDate)
