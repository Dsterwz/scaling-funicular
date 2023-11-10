from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.registerView, name="sign-up"),
    path("sign-in/", views.loginView, name="sign-in"),
    path("sign-out/", views.logoutView, name="sign-out"),

    path("my-profile/", views.my_profile, name="my-profile"),
    path("profile/<username>", views.friend_profile, name="profile"),
]