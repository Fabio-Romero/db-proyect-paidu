from django.db import models

class ResearchGroup(models.Model):
    """
    Model representing a research group.
    
    A research group is typically a collection of individuals (researchers, students, etc.) 
    who work together on specific academic or scientific research. This model holds information
    about the group such as its name and a description.
    
    Fields:
        - name: The name of the research group (must be unique).
        - description: A textual description providing details about the research group.
    """
    
    name = models.CharField(max_length=255, unique=True)  # The name of the research group. Should be unique.
    description = models.TextField(blank=True, null=True)  # A description of the research group (optional).

    def __str__(self):
        """
        String representation of the ResearchGroup instance.
        
        This method returns the name of the research group when an instance is printed or displayed.
        """
   
