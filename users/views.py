from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, UserLoginSerializer

@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={
        201: 'User created with token',
        400: 'Invalid data'
    }
)
@api_view(['POST'])
def signup(request):
    """Handle user registration and token generation"""

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=UserLoginSerializer,
    responses={
        200: 'Authentication token',
        400: 'Invalid/missing credentials',
        401: 'Invalid credentials'
    }
)
@api_view(['POST'])
def login(request):
    """Login user and return authentication token"""
    username = request.data.get('username')
    password = request.data.get('password')

    # Check for missing fields
    if not username or not password:
        return Response(
            {'detail': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Authenticate user
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

    # Invalid credentials
    return Response(
        {'detail': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED  # Updated status code
    )
