from django.shortcuts import redirect, get_object_or_404
from Djangoadvanceproject.common.models import PhotoLike, PhotoComment
from django.db import IntegrityError
from django.http import HttpResponseBadRequest
import asyncio
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from Djangoadvanceproject.photos.models import ThreeDPhoto
from django.db.models import Count
from django.views.generic import ListView
from Djangoadvanceproject.accounts.models import Profile


def like_threed_photo(request, pk):
    # Ensure that the user is authenticated
    if request.user.is_authenticated:
        # Check if the photo is already liked by the user
        threed_photo_like = PhotoLike.objects.filter(threed_photo_id=pk, user=request.user).first()

        if threed_photo_like:
            # If it exists, dislike the photo
            threed_photo_like.delete()
        else:
            # If it does not exist, create a new like
            PhotoLike.objects.create(threed_photo_id=pk, user=request.user)  # Include user here

    # Redirect back to the referring page
    return redirect(request.META.get('HTTP_REFERER') + f"#photo-{pk}")


def create_comment(request, pk):
    try:
        if request.method == "POST":
            text = request.POST.get("comment")
            threed_photo = get_object_or_404(ThreeDPhoto, pk=pk)

            if request.user.is_authenticated:
                PhotoComment.objects.create(text=text, threed_photo=threed_photo, user=request.user)
    except IntegrityError:
        return HttpResponseBadRequest("There was an error saving your comment.")
    return redirect(request.META.get('HTTP_REFERER'))


# Async function to get top liked photos
async def top_liked_photos(request):
    await asyncio.sleep(1.5)  # Simulate a delay

    # Fetch top liked photos
    top_photos = await sync_to_async(lambda: list(
        ThreeDPhoto.objects.annotate(like_count=Count('photolike')).order_by('-like_count')[:5]
    ))()

    # Prepare the response data
    photos_data = [
        {
            'photo_name': photo.photo_name,
            'url': photo.photo.url,
            'like_count': photo.like_count,
        }
        for photo in top_photos
    ]

    return JsonResponse({'photos': photos_data})


class MyPhotosView(ListView):
    model = ThreeDPhoto
    template_name = 'common/my_photos.html'
    context_object_name = 'photos'

    def get_queryset(self):
        # Get the profile of the user whose photos are being viewed
        profile_id = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_id)
        return ThreeDPhoto.objects.filter(user=profile.user)  # Assuming 'user' is a foreign key in ThreeDPhoto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.kwargs['pk']
        context['profile'] = Profile.objects.get(pk=profile_id)
        return context
