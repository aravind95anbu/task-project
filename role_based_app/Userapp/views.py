from rest_framework import viewsets, permissions
from .models import Member, Role, Right
from .serializers import MemberSerializer, RoleSerializer, RightSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class RightViewSet(viewsets.ModelViewSet):
    queryset = Right.objects.all()
    serializer_class = RightSerializer
    permission_classes = [permissions.IsAuthenticated]
