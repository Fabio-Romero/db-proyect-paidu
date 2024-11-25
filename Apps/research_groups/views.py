from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
from drf_yasg.utils import swagger_auto_schema
from .models import ResearchGroup
from .serializers import ResearchGroupSerializer
from rest_framework.decorators import api_view
from django.db.models import Q


class ResearchGroupList(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of all research groups in the system. This endpoint allows clients to get a complete list of all available research groups.",
        responses={200: ResearchGroupSerializer(many=True)},
        tags=["Research Groups"]
    )
    def get(self, request, format=None):
        """
        List all research groups in the system.
        This endpoint retrieves all research groups and returns them as a list.
        Each group is serialized to include its fields, such as name, description, and associated data.
        """
        groups = ResearchGroup.objects.all()
        serializer = ResearchGroupSerializer(groups, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new research group in the system. This endpoint accepts the necessary data to create a new group and stores it in the database.",
        request_body=ResearchGroupSerializer,
        responses={
            201: ResearchGroupSerializer,
            400: "Invalid input. Please ensure the data follows the expected structure and all required fields are included."
        },
        tags=["Research Groups"]
    )
    def post(self, request, format=None):
        """
        Create a new research group with the provided data.
        This method accepts the details of a new research group and saves it to the database.
        The request should include all required fields for a valid research group.
        """
        serializer = ResearchGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResearchGroupDetail(APIView):
    def get_object(self, pk):
        """
        Retrieve a research group instance by its primary key (pk).
        If the group is not found, an Http404 error will be raised.
        """
        try:
            return ResearchGroup.objects.get(pk=pk)
        except ResearchGroup.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="Retrieve the details of a specific research group by its unique ID.",
        responses={200: ResearchGroupSerializer, 404: "Research group not found. Ensure the provided ID is correct."},
        tags=["Research Groups"]
    )
    def get(self, request, pk, format=None):
        """
        Get details of a specific research group by its ID.
        This method retrieves the research group identified by the provided `pk` and returns its details in the response.
        """
        group = self.get_object(pk)
        serializer = ResearchGroupSerializer(group)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Fully update an existing research group. This endpoint allows the complete replacement of the existing group details with the new data provided.",
        request_body=ResearchGroupSerializer,
        responses={
            200: ResearchGroupSerializer,
            400: "Invalid input. Ensure the provided data matches the expected format and contains all required fields.",
            404: "Research group not found. The group with the specified ID could not be found."
        },
        tags=["Research Groups"]
    )
    def put(self, request, pk, format=None):
        """
        Fully update an existing research group's details.
        This method replaces all fields of the specified research group with the new data provided in the request.
        """
        group = self.get_object(pk)
        serializer = ResearchGroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update an existing research group. This allows updating only the fields provided in the request, leaving others unchanged.",
        request_body=ResearchGroupSerializer,
        responses={
            200: ResearchGroupSerializer,
            400: "Invalid input. Ensure the data format is correct and only the fields to be updated are included.",
            404: "Research group not found. The group with the specified ID could not be found."
        },
        tags=["Research Groups"]
    )
    def patch(self, request, pk, format=None):
        """
        Partially update an existing research group's details.
        This method allows you to update one or more fields of an existing research group without affecting other fields.
        """
        group = self.get_object(pk)
        serializer = ResearchGroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific research group by its unique ID. This permanently removes the research group from the database.",
        responses={204: "Research group deleted successfully.", 404: "Research group not found. The group with the specified ID could not be found."},
        tags=["Research Groups"]
    )
    def delete(self, request, pk, format=None):
        """
        Delete a specific research group by its ID.
        This method permanently removes the research group from the system.
        The `pk` parameter identifies the group to be deleted.
        """
        group = self.get_object(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def filter_research_groups_by_technology(request):
    """
    Filter research groups based on text conditions related to new technologies:
    - The name contains 'Technology', 'Innovation', or 'Development', and
    - The description includes 'implementation', 'new technologies', or 'advancement'.
    """

    # We build the text conditions with Q()
    research_groups = ResearchGroup.objects.filter(
        (Q(name__icontains="Tecnologia") | Q(name__icontains="Innovacion")) &  # Name
        (Q(description__icontains="implementacion") | Q(description__icontains="nuevas tecnologias") | Q(description__icontains="adelanto"))  # Description
    )

    # We serialize the data
    serializer = ResearchGroupSerializer(research_groups, many=True)

    # If there are no results, we return a message
    if not research_groups.exists():
        return JsonResponse({"detail": "No research groups found related to new technologies."}, status=404)

    return JsonResponse(serializer.data, safe=False)
