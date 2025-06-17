from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from .models import Department, Employee, UserDetails


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class SignupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'group_name']

    def create(self, validated_data):
        group_name = validated_data.pop("group_name", None)
        validated_data["password"] = make_password(validated_data["password"])

        user = User.objects.create(**validated_data)

        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)