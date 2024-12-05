from django.urls import path
from . import views
from Djangoadvanceproject.common.views import like_threed_photo, create_comment, MyPhotosView

urlpatterns = (

    path("threed_photo_like/<int:pk>/", like_threed_photo, name="like_threed_photo"),
    path("create_comment/<int:pk>/", create_comment, name="create_comment"),
    path('top-liked-photos/', views.top_liked_photos, name='top_liked_photos'),
    path('profile/<int:pk>/my-photos/', MyPhotosView.as_view(), name='my_photos'),
)
