from django.urls import path
from django.conf import settings
from core.views import index
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
    path("", index, name="feed") 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)