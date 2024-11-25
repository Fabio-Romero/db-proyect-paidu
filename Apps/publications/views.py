from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
from drf_yasg.utils import swagger_auto_schema
from .models import Publication
from .serializers import PublicationSerializer
from django.db.models import Q
from rest_framework.decorators import api_view
from django.db.models import Count

class PublicationList(APIView):
    """
    Handles listing all publications and creating new publications.
    """

    @swagger_auto_schema(
        operation_description="Retrieve a list of all publications.",
        responses={200: PublicationSerializer(many=True)}
    )
    def get(self, request, format=None):
        """
        List all publications in the system.
        """
        publications = Publication.objects.all()  # Fetch all publications from the database
        serializer = PublicationSerializer(publications, many=True)  # Serialize the publication data
        return Response(serializer.data)  # Return the serialized data as a response

    @swagger_auto_schema(
        operation_description="Create a new publication.",
        request_body=PublicationSerializer,
        responses={201: PublicationSerializer, 400: "Invalid input."}
    )
    def post(self, request, format=None):
        """
        Create a new publication with the provided data.
        """
        serializer = PublicationSerializer(data=request.data)  # Deserialize the input data
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the new publication to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the created data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors


class PublicationDetail(APIView):
    """
    Handles retrieving, updating, and deleting a specific publication.
    """

    def get_object(self, pk):
        """
        Retrieve a publication instance by its primary key (pk).
        """
        try:
            return Publication.objects.get(pk=pk)  # Attempt to fetch the publication by its primary key
        except Publication.DoesNotExist:
            raise Http404  # Raise a 404 error if the publication does not exist

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific publication.",
        responses={200: PublicationSerializer, 404: "Publication not found."}
    )
    def get(self, request, pk, format=None):
        """
        Get the details of a specific publication by its ID.
        """
        publication = self.get_object(pk)  # Retrieve the publication object
        serializer = PublicationSerializer(publication)  # Serialize the publication data
        return Response(serializer.data)  # Return the serialized data

    @swagger_auto_schema(
        operation_description="Update an existing publication.",
        request_body=PublicationSerializer,
        responses={200: PublicationSerializer, 400: "Invalid input.", 404: "Publication not found."}
    )
    def put(self, request, pk, format=None):
        """
        Fully update an existing publication's details.
        """
        publication = self.get_object(pk)  # Fetch the publication instance
        serializer = PublicationSerializer(publication, data=request.data)  # Deserialize the input data
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the updated data
            return Response(serializer.data)  # Return the updated publication data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

    @swagger_auto_schema(
        operation_description="Partially update an existing publication.",
        request_body=PublicationSerializer,
        responses={200: PublicationSerializer, 400: "Invalid input.", 404: "Publication not found."}
    )
    def patch(self, request, pk, format=None):
        """
        Partially update an existing publication's details.
        """
        publication = self.get_object(pk)  # Fetch the publication instance
        serializer = PublicationSerializer(publication, data=request.data, partial=True)  # Partially deserialize input data
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the updated data
            return Response(serializer.data)  # Return the updated publication data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

    @swagger_auto_schema(
        operation_description="Delete a specific publication.",
        responses={204: "Publication deleted.", 404: "Publication not found."}
    )
    def delete(self, request, pk, format=None):
        """
        Delete a publication by its ID (pk).
        """
        publication = self.get_object(pk)  # Retrieve the publication object
        publication.delete()  # Delete the publication
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return success status


@api_view(['GET'])
def filter_publications_by_word_date(request):
    """
    Filter publications containing a specific word in the title and published on or after a specified date.
    """
    title = request.GET.get('title', 'IA')  # Default filter for "IA" in the title
    start_date = request.GET.get('start_date', '2023-02-01')  # Default start date filter

    # Construct the query using Q objects
    query = Q(title__icontains=title) & Q(publication_date__gte=start_date)
    publications = Publication.objects.filter(query)  # Apply the query

    if not publications.exists():  # Check if no results are found
        return JsonResponse({"detail": "No publications found with the given criteria."}, status=404)

    serializer = PublicationSerializer(publications, many=True)  # Serialize the data
    return JsonResponse(serializer.data, safe=False)  # Return the serialized data


@api_view(['GET'])
def filter_publications_by_date_and_faculty(request):
    """
    Filter publications by publication date in 2023 and specific faculties (e.g., "Ingeniería" or "Ciencias de la Salud").
    """
    publications = Publication.objects.filter(
        Q(publication_date__year=2023) &
        (Q(user__program__faculty__name__icontains="Ingeniería") |
         Q(user__program__faculty__name__icontains="Ciencias de la Salud"))
    ).distinct()

    if not publications.exists():  # Check if no results are found
        return JsonResponse({"detail": "No publications found with the given criteria."}, status=404)

    serializer = PublicationSerializer(publications, many=True)  # Serialize the data
    return JsonResponse(serializer.data, safe=False)  # Return the serialized data


@api_view(['GET'])
def group_publications_by_research_group(request):
    """
    Group publications by research group and count the total number of publications in each group.
    """
    publications = Publication.objects.values(
        'research_group__id', 'research_group__name'
    ).annotate(total=Count('id')).order_by('-total')  # Group by research group and count publications

    return JsonResponse(list(publications), safe=False)  # Return the grouped data


@api_view(['GET'])
def group_publications_by_user_and_research_group(request):
    """
    Group publications by user and research group, counting the total publications per user in each group.
    """
    publications = Publication.objects.values(
        'user__id', 'user__first_name', 'user__last_name',
        'research_group', 'research_group__name'
    ).annotate(
        total=Count('id')  # Count publications per user in each group
    ).order_by('-total')  # Order by total count

    return JsonResponse(list(publications), safe=False)  # Return the grouped data
