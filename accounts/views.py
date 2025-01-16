from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated

class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        user = User.objects.filter(username=request.data.get('username')).first()
        if user and user.check_password(request.data.get('password')):
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED) 

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        if request.user != user_to_follow:
            if user_to_follow in request.user.following.all():
                request.user.following.remove(user_to_follow)
                return Response({'status': 'unfollowed'})
            request.user.following.add(user_to_follow)
            return Response({'status': 'followed'})
        return Response({'error': 'You cannot follow yourself'}, 
                      status=status.HTTP_400_BAD_REQUEST) 
