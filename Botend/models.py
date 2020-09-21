from django.db import models

from django.db import models


class ReportTask(models.Model):
    rid = models.AutoField('ID', primary_key=True)
    uid = models.IntegerField()
    url = models.CharField(max_length=500)
    aread = models.IntegerField(default=0)

    class Meta:
        db_table = "reports"
