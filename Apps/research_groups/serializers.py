from rest_framework import serializers
from .models import ResearchGroup

class ResearchGroupSerializer(serializers.ModelSerializer):
    """
    Serializer class for the ResearchGroup model.
    
    This class is responsible for converting `ResearchGroup` model instances 
    to Python data types (such as dictionaries) and vice versa. It also handles
    validating input data for creating or updating research groups.

    Fields:
        - All fields from the `ResearchGroup` model.
    """
    class Meta:
        model = ResearchGroup  # Specifies the model to be serialized
        fields = "__all__"     # Includes all fields from the model in the serialization
