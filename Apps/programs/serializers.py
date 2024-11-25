from rest_framework import serializers
from .models import Faculty
from .models import Program

class FacultySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Faculty model.
    Converts Faculty model instances into JSON format and vice versa.
    """
    class Meta:
        model = Faculty
        fields = "__all__"  # Includes all fields of the Faculty model in the serialized output


class ProgramSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Program model.
    Converts Program model instances into JSON format and vice versa.
    """
    # Retrieves the 'name' field from the related 'Faculty' model and makes it read-only.
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    
    class Meta:
        model = Program
        # Includes the program name, related faculty ID, and faculty name in the serialized output
        fields = ['id', 'name', 'faculty', 'faculty_name']
