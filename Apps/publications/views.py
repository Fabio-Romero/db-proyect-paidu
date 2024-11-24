from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from .models import Publication
from .serializers import PublicationSerializer

class PublicationList(APIView):
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
        responses={
            201: PublicationSerializer,
            400: "Invalid input."
        }
    )
    def post(self, request, format=None):
        """
        Create a new publication with the provided data.
        """
        serializer = PublicationSerializer(data=request.data)  # Deserialize the input data into a publication instance
        if serializer.is_valid():  # Check if the data is valid
            serializer.save()  # Save the new publication to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the created publication data with 201 status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if validation fails


class PublicationDetail(APIView):
    def get_object(self, pk):
        """
        Retrieve a publication instance by its primary key (pk).
        """
        try:
            return Publication.objects.get(pk=pk)  # Attempt to fetch the publication by its pk
        except Publication.DoesNotExist:
            raise Http404  # Raise a 404 error if the publication does not exist

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific publication.",
        responses={200: PublicationSerializer, 404: "Publication not found."}
    )
    def get(self, request, pk, format=None):
        """
        Get the details of a specific publication by its ID (pk).
        """
        publication = self.get_object(pk)  # Get the publication object
        serializer = PublicationSerializer(publication)  # Serialize the publication data
        return Response(serializer.data)  # Return the serialized publication data

    @swagger_auto_schema(
        operation_description="Update an existing publication.",
        request_body=PublicationSerializer,
        responses={
            200: PublicationSerializer,
            400: "Invalid input.",
            404: "Publication not found."
        }
    )
    def put(self, request, pk, format=None):
        """
        Fully update an existing publication's details.
        """
        publication = self.get_object(pk)  # Fetch the publication instance by its pk
        serializer = PublicationSerializer(publication, data=request.data)  # Deserialize the input data for the existing publication
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the updated publication data
            return Response(serializer.data)  # Return the updated publication data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if validation fails

    @swagger_auto_schema(
        operation_description="Partially update an existing publication.",
        request_body=PublicationSerializer,
        responses={
            200: PublicationSerializer,
            400: "Invalid input.",
            404: "Publication not found."
        }
    )
    def patch(self, request, pk, format=None):
        """
        Partially update an existing publication's details.
        """
        publication = self.get_object(pk)  # Fetch the publication instance by its pk
        serializer = PublicationSerializer(publication, data=request.data, partial=True)  # Partially deserialize the input data
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the partially updated publication data
            return Response(serializer.data)  # Return the updated publication data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if validation fails

    @swagger_auto_schema(
        operation_description="Delete a specific publication.",
        responses={204: "Publication deleted.", 404: "Publication not found."}
    )
    def delete(self, request, pk, format=None):
        """
        Delete a publication by its ID (pk).
        """
        publication = self.get_object(pk)  # Fetch the publication instance by its pk
        publication.delete()  # Delete the publication from the database
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return a 204 status indicating successful deletion
