from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import UserSerializer

# View to handle listing all users and creating new users
class UserList(APIView):
    """
    Handles operations for retrieving all users and creating new users.
    """
    @swagger_auto_schema(
        operation_description="Retrieve a list of all users, including their related programs.",
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request, format=None):
        """
        Fetches all user instances from the database, including their related program data.
        The response includes serialized JSON data of all users.
        """
        users = User.objects.select_related('program') # Optimized query to include related program data
        serializer = UserSerializer(users, many=True) # Serialize multiple user objects
        return Response(serializer.data) # Return serialized data in JSON format

    @swagger_auto_schema(
        operation_description="Create a new user.",
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: "Invalid input."
        }
    )
    def post(self, request, format=None):
        """
        Creates a new user with the provided JSON data.
        Validates the incoming data against the UserSerializer and saves it to the database if valid.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Handles operations for retrieving, updating, and deleting specific users by ID.
    """
    def get_object(self, pk):
        """
        Helper method to fetch a user instance by primary key (pk).
        If the user does not exist, raises an Http404 exception.
        """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific user.",
        responses={200: UserSerializer, 404: "User not found."}
    )
    def get(self, request, pk, format=None):
        """
        Fetches the details of a specific user by their primary key (ID).
        Returns serialized JSON data of the user.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update an existing user completely.",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Invalid input.",
            404: "User not found."
        }
    )
    def put(self, request, pk, format=None):
        """
        Fully updates a user's details by replacing the existing data with the provided JSON data.
        Validates the input data and updates the database entry if valid.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update an existing user's details.",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Invalid input.",
            404: "User not found."
        }
    )
    def patch(self, request, pk, format=None):
        """
        Partially updates a user's details with the provided JSON data.
        Only the fields included in the request are updated.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific user.",
        responses={204: "User deleted successfully.", 404: "User not found."}
    )
    def delete(self, request, pk, format=None):
        """
        Deletes a user by their primary key (ID) from the database.
        Returns a 204 No Content status if successful.
        """
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
