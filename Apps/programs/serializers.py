from rest_framework import serializers
from .models import Faculty
from .models import Program

class FacultySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Faculty model.
    """
    class Meta:
        model = Faculty
        fields = "__all__"


class ProgramSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Program model.
    """
    # Retrieves the 'name' field from the related 'program' model and makes it read-only.
    faculty_name= serializers.CharField(source='faculty.name',read_only=True) 
    class Meta:
        model = Program
        fields = ['name','faculty','faculty_name']
