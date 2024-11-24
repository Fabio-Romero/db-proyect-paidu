from rest_framework import serializers
from .models import Publication

class PublicationSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Publication model.
    This class is used to convert Publication instances to JSON format
    and vice versa. It also handles nested relationships for user and research group.
    """
    # Using a nested serializer method to return the full name of the user
    user_name = serializers.SerializerMethodField()

    # Automatically retrieves and represents the related research group's name
    research_group_name = serializers.CharField(source='research_group.name', read_only=True)

    class Meta:
        model = Publication
        fields = [
            'id',                # The unique ID of the publication
            'title',             # The title of the publication
            'abstract',          # The abstract or summary of the publication
            'publication_date',  # The date when the publication was made
            'user',              # The associated user (nested data)
            'user_name',         # The full name of the user (calculated field)
            'research_group',    # The associated research group (nested data)
            'research_group_name', # The name of the associated research group
        ]

    def get_user_name(self, obj):
        """
        Custom method to return the full name of the user.
        It concatenates the first and last names of the user.
        """
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return None
