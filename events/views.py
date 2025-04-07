from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Event, Registration
from .serializers import EventSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


header_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description='Authorization header with token (e.g., "Token <your token>")',
    type=openapi.TYPE_STRING,
)


@swagger_auto_schema(
    method='get',
    manual_parameters=[header_param]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_events(request):
    """Get all events (authenticated users only)"""
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    manual_parameters=[header_param]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event(request, event_id):
    """Get single event by ID (authenticated users only)"""
    event = get_object_or_404(Event, pk=event_id)
    serializer = EventSerializer(event)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    request_body=EventSerializer,
    manual_parameters=[header_param]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    """Create new event (authenticated users only)"""
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(organizer=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
    request_body=EventSerializer,
    manual_parameters=[header_param]
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event(request, event_id):
    """Update event (only organizer can update)"""
    event = get_object_or_404(Event, pk=event_id)

    if request.user != event.organizer:
        return Response(
            {'detail': 'You do not have permission to perform this action.'},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = EventSerializer(event, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='delete',
    manual_parameters=[header_param]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, event_id):
    """Delete event (only organizer can delete)"""
    event = get_object_or_404(Event, pk=event_id)

    if request.user != event.organizer:
        return Response(
            {'detail': 'You do not have permission to perform this action.'},
            status=status.HTTP_403_FORBIDDEN
        )

    event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='post',
    manual_parameters=[header_param]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_for_event(request, event_id):
    """Register authenticated user for an event"""
    event = get_object_or_404(Event, pk=event_id)

    # Check existing registration
    if Registration.objects.filter(user=request.user, event=event).exists():
        return Response(
            {'error': 'You are already registered for this event'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create registration
    registration = Registration.objects.create(
        user=request.user,
        event=event
    )

    return Response(
        {'message': 'Successfully registered for the event', 'registration_id': registration.id},
        status=status.HTTP_201_CREATED
    )

@swagger_auto_schema(
    method='get',
    manual_parameters=[header_param]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_registered_events(request):
    """List all events the current user has registered for"""
    registrations = Registration.objects.filter(user=request.user)
    events = [reg.event for reg in registrations]
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)