from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views  # Keep only your app's views

router = DefaultRouter()
router.register(r'Employee', views.EmployeeViewSet)
router.register(r'Department', views.DepartmentViewSet)
router.register(r'Userdetails', views.UserViewSet)

urlpatterns = [
    path("signup/", views.SignupAPIView.as_view(), name="user-signup"),
    path("login/", views.LoginAPIView.as_view(), name="user-login"),
]

urlpatterns += router.urls