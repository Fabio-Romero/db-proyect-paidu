from django.db import models

class Faculty(models.Model):
    # Faculty name, must be unique
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        # Returns the faculty name as its string representation
        return self.name


class Program(models.Model):
    # Academic program name, must be unique
    name = models.CharField(max_length=255, unique=True)
    # Relationship with the Faculty model (ForeignKey), deletes the program if the related faculty is deleted
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        # Returns the program name as its string representation
        return self.name
