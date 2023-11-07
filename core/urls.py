from django.urls import path
from django.conf import settings
from core import views
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
    path("", views.index, name="feed"),

    # Ajax URLs
    path("create-post/", views.create_post, name="create-post"),
    path("like-post/", views.like_post, name="like-post"),
    path("comment-post/", views.comment_on_post, name="comment-post"),
    path("like-comment/", views.like_comment, name="like-comment"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)