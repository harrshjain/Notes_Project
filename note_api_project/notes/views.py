from rest_framework import generics, permissions, status
from .models import Note
from .serializers import NoteSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.throttling import UserRateThrottle

class SignUpView(APIView):
    throttle_classes = [UserRateThrottle]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'This username is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        Token.objects.create(user=user)  # Create a token for the new user

        return Response({'token': str(user.auth_token)}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    throttle_classes = [UserRateThrottle]
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'token': str(user.auth_token)}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class NoteListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

class NoteShareView(generics.UpdateAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ensure the note belongs to the authenticated user
        queryset = self.get_queryset().filter(user=self.request.user)
        return generics.get_object_or_404(queryset, pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        shared_user_id = request.data.get('shared_user_id')

        if shared_user_id is None:
            return Response({'error': 'shared_user_id is required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

        shared_user = generics.get_object_or_404(User, id=shared_user_id)

        instance.shared_with.add(shared_user)
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class NoteSearchView(generics.ListAPIView):
    throttle_classes = [UserRateThrottle]
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Note.objects.filter(user=self.request.user, content__icontains=query)

class NoteDeleteView(generics.DestroyAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ensure the note belongs to the authenticated user
        queryset = self.get_queryset().filter(user=self.request.user)
        return generics.get_object_or_404(queryset, pk=self.kwargs['pk'])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Note deleted successfully.'}, status=status.HTTP_200_OK)
    
class NoteUpdateView(generics.UpdateAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ensure the note belongs to the authenticated user
        queryset = self.get_queryset().filter(user=self.request.user)
        return generics.get_object_or_404(queryset, pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)