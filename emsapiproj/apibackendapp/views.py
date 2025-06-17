from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters, permissions
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group

from .models import Employee, Department, UserDetails
from .serializers import (
    EmployeeSerializer,
    DepartmentSerializer,
    UserSerializer,
    UserDetailsSerializer,
    SignupSerializer,
    LoginSerializer,
)

# ViewSets
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['EmployeeName', 'Designation']
    permission_classes = [permissions.IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# API Views
class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "user_id": user.id,
                "username": user.username,
                "token": token.key,
                "role": user.groups.first().id if user.groups.exists() else None
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "username": user.username,
                    "role": user.groups.first().id if user.groups.exists() else None,
                    "data": {
                        "Token": token.key
                    }
                }, status=status.HTTP_200_OK)

            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Invalid username or password"
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)