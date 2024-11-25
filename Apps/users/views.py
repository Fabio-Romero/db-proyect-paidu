from Apps.publications.models import Publication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import UserSerializer
from django.db.models import Count
from rest_framework.decorators import api_view

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
        """
        users = User.objects.select_related('program')  # Optimized query to include related program data
        serializer = UserSerializer(users, many=True)  # Serialize multiple user objects
        return Response(serializer.data)  # Return serialized data in JSON format

    @swagger_auto_schema(
        operation_description="Create a new user.",
        request_body=UserSerializer,
        responses={201: UserSerializer, 400: "Invalid input."}
    )
    def post(self, request, format=None):
        """
        Creates a new user with the provided JSON data.
        """
        serializer = UserSerializer(data=request.data)  # Deserialize input data
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the user to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return created data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors


class UserDetail(APIView):
    """
    Handles operations for retrieving, updating, and deleting specific users by ID.
    """
    def get_object(self, pk):
        """
        Helper method to fetch a user instance by primary key (pk).
        """
        try:
            return User.objects.get(pk=pk)  # Fetch the user by primary key
        except User.DoesNotExist:
            raise Http404  # Raise an error if the user is not found

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific user.",
        responses={200: UserSerializer, 404: "User not found."}
    )
    def get(self, request, pk, format=None):
        """
        Fetches the details of a specific user by their ID.
        """
        user = self.get_object(pk)  # Get the user object
        serializer = UserSerializer(user)  # Serialize the user data
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update an existing user completely.",
        request_body=UserSerializer,
        responses={200: UserSerializer, 400: "Invalid input.", 404: "User not found."}
    )
    def put(self, request, pk, format=None):
        """
        Fully updates a user's details with the provided JSON data.
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
        responses={200: UserSerializer, 400: "Invalid input.", 404: "User not found."}
    )
    def patch(self, request, pk, format=None):
        """
        Partially updates a user's details with the provided JSON data.
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
        """
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def users_by_program(request, program_id):
    """
    Retrieve all users belonging to a specific program by program ID.
    """
    users = User.objects.filter(program_id=program_id)  # Filter users by program ID
    if not users.exists():
        return JsonResponse(
            {"detail": f"No users found for the program with ID: {program_id}"},
            status=404
        )
    
    serializer = UserSerializer(users, many=True)  # Serialize the user data
    return JsonResponse(serializer.data, safe=False)  # Return the serialized data


@api_view(['GET'])
def group_users_by_research_group_filtered(request):
    """
    Group users by research group through publications and count the total users per group.
    Includes only students in programs related to "Ingeniería".
    """
    groups = Publication.objects.filter(
        user__user_type="student",  # Filter only users of type "student"
        user__program__faculty__name__icontains="Ingeniería"  # Filter users in programs related to "Ingeniería"
    ).values(
        'research_group', 'research_group__name'  # Include research group ID and name
    ).annotate(
        total=Count('user', distinct=True)  # Count distinct users per group
    ).order_by('-total')  # Order groups by total user count

    return JsonResponse(list(groups), safe=False)  # Return grouped data
