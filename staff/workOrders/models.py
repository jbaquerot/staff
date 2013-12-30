from django.db import models

# Create your models here.

class WorkOrder(models.Model):
	processed = models.NullBooleanField(default=False)
	staffId = models.CharField(max_length=6)
	woDate = models.DateField()
	total_No_Taxes = models.FloatField()
	woFile = models.FileField(upload_to='documents/%Y/%m/%d')

	def __unicode__(self):
		return self.staffId + ':' + str(self.woDate)


class Order(models.Model):
	workOrder = models.ForeignKey(WorkOrder)
	staffId = models.CharField(max_length=6)
	project = models.CharField(max_length=30)
	woDate = models.DateField()
	hours = models.FloatField()
	perctHours = models.FloatField()
	total = models.FloatField()

	#def __unicode__(self):
	#	return self.staffId + ':'+ self.project + ':' +str(self.woDate)
