from django.urls import path
from user.views import CreateUserView, LoginUserView, ManageUserView
from rest_framework.authtoken import views

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="get_token"),
    path("profile/", ManageUserView.as_view(), name="manage_user")
]

