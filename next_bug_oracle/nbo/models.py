from django.db import models


class Bug(models.Model):
    bug_id = models.IntegerField(primary_key=True)
    bug_text = models.TextField
    report_date = models.DateTimeField
    source = models.CharField(max_length=8)
    link = models.URLField

    def __str__(self):
        return self.bug_id + ': ' + self.bug_text
