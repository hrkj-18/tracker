from datetime import datetime
from django.db import models


# Create your models here.


class WorkItem(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    has_IA = models.BooleanField(default=False)
    has_CR = models.BooleanField(default=False)
    created = models.DateTimeField(default=datetime.now())
    description = models.TextField(default='')
    owner = models.CharField(max_length=200, null=False, default='')
    in_DM = models.BooleanField(default=0)
    hours = models.IntegerField(default=0)
    ad_work_package = models.CharField(max_length=50, null=False, default='')
    '''owners end date'''


class Comment(models.Model):
    work_item = models.ForeignKey(WorkItem, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[0:15]
