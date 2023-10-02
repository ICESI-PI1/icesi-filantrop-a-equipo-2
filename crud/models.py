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
    

class Student(models.Model):
    student_code = models.CharField(max_length=9,
                                    null=False,
                                    blank=False)
    
    name = models.CharField(max_length=100,
                            null=False,
                            blank=False)
    
    ID_OPTIONS = [
        ('PA', 'PA - Pasaporte'),
        ('CC', 'CC - Cédula de Ciudadanía'),
        ('TI', 'TI - Tarjeta de Identidad'),
        ('CE', 'CE - Cédula de Extranjería'),
        ('RC', 'RC - Registro Civil'),
    ]

    id_type = models.CharField(max_length=2,
                                null=False,
                                blank=False,
                                choices=ID_OPTIONS)
    
    email = models.CharField(max_length=1000,
                                null=False,
                                blank=False)
    
    institutional_email = models.CharField(max_length=1000,
                                           null=False,
                                           blank=False)
    
    icfes_score = models.IntegerField(null=False,
                                      blank=False)
    
    birth_date = models.DateField(null=False,
                                  blank=False)
    
    cellphone_number = models.CharField(max_length=15,
                                        null=False,
                                        blank=False)
    
    accumulated_average = models.DecimalField(max_digits=2,
                                              decimal_places=1,
                                              null=False)
    
    credits_studied = models.IntegerField(null=False)

    def __str__(self):
        return self.name + " - " + self.student_code