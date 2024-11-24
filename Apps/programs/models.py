from django.db import models

class Faculty(models.Model):
    # Nombre de la facultad, único
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Program(models.Model):
    # Nombre del programa académico, único
    name = models.CharField(max_length=255, unique=True)
    # Relación con la facultad (ForeignKey) que elimina el programa si se elimina la facultad
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
