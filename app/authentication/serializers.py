from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Django Group Model
    """
    url = serializers.HyperlinkedIdentityField(view_name="api:group-detail")

    class Meta:
        model = Group
        fields = ['url', 'name', ]


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Django Permission Model
    """
    url = serializers.HyperlinkedIdentityField(view_name="api:permission-detail")

    class Meta:
        model = Permission
        fields = ['url', 'name', ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Django User Model
    """
    url = serializers.HyperlinkedIdentityField(view_name="api:user-detail")
    groups = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='auth:group-detail',
    )

    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name',
                  'email', 'groups', 'last_login', 'is_superuser',
                  'is_active', ]
