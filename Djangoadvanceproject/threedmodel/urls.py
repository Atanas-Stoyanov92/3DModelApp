from django.urls import path, include

from Djangoadvanceproject.threedmodel.views import ThreeDModelCreateView, ThreeDModelDetailView, ThreeDModelDeleteView, \
    ThreeDModelEditView

urlpatterns = (
    path("create-threedmodel/", ThreeDModelCreateView.as_view(), name="create threedmodel"),
    path("threedmodel/<slug:threedmodel_slug>/",
         include([
             path("", ThreeDModelDetailView.as_view(), name='details threedmodel'),
             path("edit/", ThreeDModelEditView.as_view(), name='edit threedmodel'),
             path("delete/", ThreeDModelDeleteView.as_view(), name='delete threedmodel'),
         ])),
)
