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


class NonAcademicActvitiesReport(models.Model):
    student_code = models.CharField(max_length=9,
                                    null=False,
                                    blank=False)

    name = models.CharField(max_length=100,
                            null=False,
                            blank=False)

    lastname = models.CharField(max_length=100,
                                null=False,
                                blank=False)

    activity = models.CharField(max_length=100,
                                null=False,
                                blank=False)

    activity_hours = models.DecimalField(max_digits=3,
                                         decimal_places=1,
                                         null=False,
                                         blank=False)

    semester = models.CharField(max_length=6,
                                null=False,
                                blank=False)

    def str(self):
        return self.name + " " + self.lastname + " - " + self.activity + " - " + self.semester


class CREAReport(models.Model):
    student_code = models.CharField(max_length=9,
                                    null=False,
                                    blank=False)

    name = models.CharField(max_length=100,
                            null=False,
                            blank=False)

    lastname = models.CharField(max_length=100,
                                null=False,
                                blank=False)

    monitor_name = models.CharField(max_length=100,
                                    null=False,
                                    blank=False)

    reason = models.CharField(max_length=500,
                              null=False,
                              blank=False)

    result = models.CharField(max_length=500,
                              null=False,
                              blank=False)

    date = models.DateField(null=False,
                            blank=False)

    hour = models.TimeField(null=False,
                            blank=False)

    def __str__(self):
        return "{} - {} - {}".format(self.student_code, self.date, self.monitor_name)

    
class Document(models.Model):
    codigo_estudiante = models.ForeignKey('Student', on_delete=models.CASCADE)
    uploadedFile = models.FileField(upload_to="Uploaded Files/")
    dateTimeOfUpload = models.DateTimeField(auto_now=True)  


class Donor(models.Model):
    nit = models.CharField(max_length=12,
                           null=False,
                           blank=False,
                           unique=True)

    name = models.CharField(max_length=100,
                            null=False,
                            blank=False)

    lastname = models.CharField(max_length=100,
                                null=False,
                                blank=False)

    email = models.EmailField(max_length=1000,
                              null=False,
                              blank=False)

    TYPE_OPTIONS = [
        ('Natural', 'Natural'),
        ('Legal', 'Legal'),
    ]

    type = models.CharField(max_length=7,
                            null=False,
                            blank=False,
                            choices=TYPE_OPTIONS)

    description = models.CharField(max_length=1000,
                                   null=False,
                                   blank=False)

    previous_colaborations = models.CharField(max_length=1000,
                                              null=False,
                                              blank=False)

    def __str__(self):
        return "{} - {} {}".format(self.nit, self.name, self.lastname)
