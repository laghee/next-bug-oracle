from django.db import models

# Create your models here.


class Bug(models.Model):
    bug_num = models.IntegerField
    bug_text = models.TextField
    bug_date = models.DateTimeField
    bug_source = models.CharField(max_length=8)
    bug_link = models.URLField

    def __str__(self):
        return self.bug_num + ': ' + self.bug_text
