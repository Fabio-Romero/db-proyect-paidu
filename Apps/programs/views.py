from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from .models import Faculty, Program
from .serializers import FacultySerializer, ProgramSerializer


class FacultyList(APIView):
    """
    Handles listing all faculties and creating new faculties.
    """

    @swagger_auto_schema(
        operation_description="Retrieve a list of all faculties.",
        responses={200: FacultySerializer(many=True)}
    )
    def get(self, request, format=None):
        """
        Retrieve a list of all faculties.
        """
        faculties = Faculty.objects.all()  # Fetch all faculty records
        serializer = FacultySerializer(faculties, many=True)  # Serialize the data
        return Response(serializer.data)  # Return serialized data as response

    @swagger_auto_schema(
        operation_description="Create a new faculty.",
        request_body=FacultySerializer,
        responses={
            201: FacultySerializer,
            400: "Invalid input."
        }
    )
    def post(self, request, format=None):
        """
        Create a new faculty.
        """
        serializer = FacultySerializer(data=request.data)  # Deserialize input data
        if serializer.is_valid():  # Validate the input
            serializer.save()  # Save the new faculty
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return success response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors


class FacultyDetail(APIView):
    """
    Handles retrieving, updating, and deleting a specific faculty.
    """

    def get_object(self, pk):
        """
        Retrieve a specific faculty by primary key (pk).
        """
        try:
            return Faculty.objects.get(pk=pk)  # Fetch faculty by primary key
        except Faculty.DoesNotExist:  # Handle case when faculty is not found
            raise Http404

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific faculty.",
        responses={200: FacultySerializer, 404: "Faculty not found."}
    )
    def get(self, request, pk, format=None):
        """
        Retrieve details of a specific faculty.
        """
        faculty = self.get_object(pk)  # Get the faculty object
        serializer = FacultySerializer(faculty)  # Serialize the data
        return Response(serializer.data)  # Return serialized data

    @swagger_auto_schema(
        operation_description="Update an existing faculty.",
        request_body=FacultySerializer,
        responses={
            200: FacultySerializer,
            400: "Invalid input.",
            404: "Faculty not found."
        }
    )
    def put(self, request, pk, format=None):
        """
        Update an existing faculty's data.
        """
        faculty = self.get_object(pk)  # Get the faculty object
        serializer = FacultySerializer(faculty, data=request.data)  # Deserialize input data
        if serializer.is_valid():  # Validate the input
            serializer.save()  # Save the updated faculty
            return Response(serializer.data)  # Return updated data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

    @swagger_auto_schema(
        operation_description="Delete a specific faculty.",
        responses={204: "Faculty deleted.", 404: "Faculty not found."}
    )
    def delete(self, request, pk, format=None):
        """
        Delete a specific faculty.
        """
        faculty = self.get_object(pk)  # Get the faculty object
        faculty.delete()  # Delete the faculty
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return no content status


class ProgramList(APIView):
    """
    Handles listing all programs and creating new programs.
    """

    @swagger_auto_schema(
        operation_description="Retrieve a list of all programs.",
        responses={200: ProgramSerializer(many=True)}
    )
    def get(self, request, format=None):
        """
        Retrieve a list of all programs.
        """
        programs = Program.objects.all()  # Fetch all program records
        serializer = ProgramSerializer(programs, many=True)  # Serialize the data
        return Response(serializer.data)  # Return serialized data as response

    @swagger_auto_schema(
        operation_description="Create a new program.",
        request_body=ProgramSerializer,
        responses={
            201: ProgramSerializer,
            400: "Invalid input."
        }
    )
    def post(self, request, format=None):
        """
        Create a new program.
        """
        serializer = ProgramSerializer(data=request.data)  # Deserialize input data
        if serializer.is_valid():  # Validate the input
            serializer.save()  # Save the new program
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return success response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors


class ProgramDetail(APIView):
    """
    Handles retrieving, updating, and deleting a specific program.
    """

    def get_object(self, pk):
        """
        Retrieve a specific program by primary key (pk).
        """
        try:
            return Program.objects.get(pk=pk)  # Fetch program by primary key
        except Program.DoesNotExist:  # Handle case when program is not found
            raise Http404

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific program.",
        responses={200: ProgramSerializer, 404: "Program not found."}
    )
    def get(self, request, pk, format=None):
        """
        Retrieve details of a specific program.
        """
        program = self.get_object(pk)  # Get the program object
        serializer = ProgramSerializer(program)  # Serialize the data
        return Response(serializer.data)  # Return serialized data

    @swagger_auto_schema(
        operation_description="Update an existing program.",
        request_body=ProgramSerializer,
        responses={
            200: ProgramSerializer,
            400: "Invalid input.",
            404: "Program not found."
        }
    )
    def put(self, request, pk, format=None):
        """
        Update an existing program's data.
        """
        program = self.get_object(pk)  # Get the program object
        serializer = ProgramSerializer(program, data=request.data)  # Deserialize input data
        if serializer.is_valid():  # Validate the input
            serializer.save()  # Save the updated program
            return Response(serializer.data)  # Return updated data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

    @swagger_auto_schema(
        operation_description="Partially update an existing program.",
        request_body=ProgramSerializer,
        responses={
            200: ProgramSerializer,
            400: "Invalid input.",
            404: "Program not found."
        }
    )
    def patch(self, request, pk, format=None):
        """
        Partially update an existing program's data.
        """
        program = self.get_object(pk)  # Get the program object
        serializer = ProgramSerializer(program, data=request.data, partial=True)  # Deserialize input data for partial update
        if serializer.is_valid():  # Validate the input
            serializer.save()  # Save the updated program
            return Response(serializer.data)  # Return updated data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

    @swagger_auto_schema(
        operation_description="Delete a specific program.",
        responses={204: "Program deleted.", 404: "Program not found."}
    )
    def delete(self, request, pk, format=None):
        """
        Delete a specific program.
        """
        program = self.get_object(pk)  # Get the program object
        program.delete()  # Delete the program
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return no content status

