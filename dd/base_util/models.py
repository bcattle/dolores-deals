from django.db import models
from django.contrib.auth.models import User

class Picture(models.Model):
	pic = models.ImageField(upload_to='uploadpics')
	created = models.DateTimeField(auto_now_add=True)
	createdBy = models.ForeignKey(User)
	related = models.ManyToManyField('self', blank=True, null=True)
	description = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return str(self.id) + ' : ' + str(self.created)
	class Meta:
		ordering = ['created']