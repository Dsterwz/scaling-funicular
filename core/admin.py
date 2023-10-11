from django.contrib import admin
from core.models import Post, Gallery


class GalleryAdminTab(admin.TabularInline):
    model = Gallery


class PostAdmin(admin.ModelAdmin):
    inlines = [GalleryAdminTab]
    list_editable = ["active"]
    list_display = ["thumbnail", "user", "title", "visibility", "active"]
    prepopulated_fields = {"slug": ("title", )}


class GalleryAdmin(admin.ModelAdmin):
    list_editable = ["active"]
    list_display = ["thumbnail", "post", "active"]


admin.site.register(Post, PostAdmin)
admin.site.register(Gallery, GalleryAdmin)
