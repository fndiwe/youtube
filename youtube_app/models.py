from django.db import models


# Create your models here.
class Suggestions(models.Model):
    words = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.words

