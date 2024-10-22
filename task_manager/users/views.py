from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

from .serializers import UserBasicSerializer


@api_view(["POST"])
def signup(request: Request):
    """API endpoint for sign-up"""

    serializer = UserBasicSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
