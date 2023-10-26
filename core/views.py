from django.shortcuts import render, redirect
from core.models import Post
from django.utils.text import slugify
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import shortuuid


@login_required
def index(request):
    posts = Post.objects.filter(active=True, visibility="Everyone")
    context = {"posts": posts}
    return render(request, "core/index.html", context)


@csrf_exempt
def create_post(request):

    if request.method == 'POST':
        title = request.POST.get('post-caption')
        visibility = request.POST.get('visibility')
        image = request.FILES.get('post-thumbnail')

        print("Title ============", title)
        print("thumbnail ============", image)
        print("visibility ============", visibility)

        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]

        if title and image:
            post = Post(
                title=title,
                visibility=visibility,
                image=image,
                user=request.user,
                slug=slugify(title) + "-" + str(uniqueid.lower())
            )
            post.save()

            return JsonResponse({"post": {
                "title": post.title,
                "image": post.image.url,
                "full_name": post.user.profile.full_name,
                "profile_image": post.user.profile.image.url,
                "date": timesince(post.date),
                "id": post.id,
            }})

        else:
            return JsonResponse({"error": "Image or title does not exist"})

    return JsonResponse({"data": "sent"})


def like_post(request):
    id = request.GET['id']
    post = Post.objects.get(id=id)
    user = request.user
    liked = False

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    data = {
        "liked": liked,
        "likes": post.likes.all().count()
    }

    return JsonResponse({"data": data})
