from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User model.
    This class defines how the User model is converted into JSON data and vice versa.
    """

    # Retrieves the 'name' field from the related 'program' model and makes it read-only.
    program_name = serializers.CharField(source='program.name', read_only=True)
    
    class Meta:
        model = User  # Specifies the model that the serializer will represent.
        fields = [
            'id',           # User's ID (automatic field).
            'first_name',   # User's first name.
            'last_name',    # User's last name.
            'email',        # User's email address.
            'program',      # Program the user belongs to (ForeignKey).
            'program_name', # Name of the related program (extracted from the related model).
            'user_type',    # Type of user (admin, researcher, student).
        ]



        
