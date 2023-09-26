from django.db import models

# Create your models here.

class Office(models.Model):
    name = models.CharField(max_length=25,
                            null=False,
                            blank=False)
    
    email = models.CharField(max_length=1000,
                            null=False,
                            blank=False)

    def __str__(self):
        return self.name