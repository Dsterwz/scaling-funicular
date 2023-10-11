from django.db import models
from userauths.models import User, Profile, user_directory_path
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe, format_html
from django.utils.text import slugify

import shortuuid

VISIBILITY = (
    ("Only me", "Only me"),
    ("Everyone", "Everyone"),
)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True)
    video = models.FileField(
        upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(
        max_length=10, default="everyone", choices=VISIBILITY)
    pid = ShortUUIDField(length=7, max_length=25,
                         alphabet="abcdefghijklmnopqrstuvxyz123")
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Post"

    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:6]
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) + "-" + str(uniqueid.lower())
        super(Post, self).save(*args, **kwargs)

    def thumbnail(self):
        return format_html('<img src="/media/{}" style="width: 50px; height: 50px; border-radius: 5px; object-fit: cover" />'.format(self.image))
        # return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />' % (self.image))


class Gallery(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="gallery", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.post)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Gallery"

    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 30px;" />' % (self.image))
