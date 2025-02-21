from rest_framework import serializers
from .models import Member, Role, Right

class RightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Right
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    rights = serializers.PrimaryKeyRelatedField(many=True, queryset=Right.objects.all())

    class Meta:
        model = Role
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = Member
        fields = ['id', 'username', 'role']
