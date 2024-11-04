from django.urls import path, include
from Djangoadvanceproject.photos.views import ThreeDPhotoCreateView, ThreeDPhotoDetailView, ThreeDPhotoEditView, \
    ThreeDPhotoDeleteView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = (
    path("create-photo/", ThreeDPhotoCreateView.as_view(), name="create photo"),
    path(
        "photos/<int:pk>/",
        include([
            path("", ThreeDPhotoDetailView.as_view(), name="details photo"),
            path("edit/", ThreeDPhotoEditView.as_view(), name="edit photo"),
            path("delete/", ThreeDPhotoDeleteView.as_view(), name="delete photo"),
        ]),
    ),
)
