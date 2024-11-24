from django.db import models
from Apps.users.models import User
from Apps.research_groups.models import ResearchGroup

class Publication(models.Model):
    """
    Model for a research publication associated with a research group and a user.
    """
    title = models.CharField(max_length=255)
    # Title of the publication (required, up to 255 characters).

    abstract = models.TextField(blank=True, null=True)
    # Optional abstract or summary of the publication.

    publication_date = models.DateField()
    # Publication date (required).

    research_group = models.ForeignKey(ResearchGroup, on_delete=models.CASCADE)
    # Linked research group; deleted with the group.

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Linked user (author); deleted with the user.

    def __str__(self):
        """
        Returns the title of the publication.
        """
        return self.title
