from django.db import models

# Create your models here.

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
	staffId = models.CharField(max_length=6)
	woDate = models.DateField(auto_now=True)
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
