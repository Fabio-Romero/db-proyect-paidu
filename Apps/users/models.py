from django.db import models
from Apps.programs.models import Program

class User(models.Model):
    """
    User model representing a user in the system. A user can be an admin, researcher, or student.
    This model includes the user's basic information and their associated program.
    """

    # Choices for user types (admin, researcher, or student)
    USER_TYPES = [
        ('admin', 'Admin'),         # Admin user type
        ('researcher', 'Researcher'),  # Researcher user type
        ('student', 'Student'),     # Student user type
    ]

    # Fields for the User model
    first_name = models.CharField(max_length=100)  # User's first name
    last_name = models.CharField(max_length=100)   # User's last name
    email = models.EmailField(unique=True)         # User's email (must be unique)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)  # User's associated program (can be null)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)  # Type of user (admin, researcher, student)

    def __str__(self):
        # String representation of the User model
        return f"{self.first_name} {self.last_name}"
