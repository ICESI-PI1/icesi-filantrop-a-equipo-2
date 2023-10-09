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

    GENRE = [
        ('M', 'M - Masculino'),
        ('F', 'F - Femenino'),
        ('O', 'O - Otro'),
    ]

    genre = models.CharField(max_length=1,
                             choices=GENRE,
                             null=False,
                             blank=False)

    id_type = models.CharField(max_length=2,
                               null=False,
                               blank=False,
                               choices=ID_OPTIONS)

    id_number = models.CharField(max_length=20,
                                 null=False,
                                 blank=False)

    email = models.EmailField(max_length=1000,
                              null=False,
                              blank=False)

    institutional_email = models.EmailField(max_length=1000,
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
                                              null=False,
                                              blank=False)

    credits_studied = models.IntegerField(null=False,
                                          blank=False)

    def __str__(self):
        return self.name + " - " + self.student_code


class Beca(models.Model):
    id_estudiante = models.CharField(max_length=20)
    tipo_beca = models.CharField(max_length=255)
    duracion = models.IntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)



def __str__(self): 
    return self.id_estudiante


class Archivo(models.Model):
    nombre = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)

