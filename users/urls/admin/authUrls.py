from django.urls import path
from users.views.admin.authentication import (
    LoginUser,
    LogoutUser,
    CreateAdminUser,
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "users"

urlpatterns = [
    path("create-admin/", CreateAdminUser.as_view(), name="create-admin"),
    path("login/", LoginUser.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutUser.as_view(), name="logout"),
]
