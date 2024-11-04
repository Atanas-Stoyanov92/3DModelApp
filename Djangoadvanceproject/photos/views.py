from django.urls import reverse
from django.views import generic as views
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixin

from Djangoadvanceproject.accounts.views import OwnerRequiredMixin
from Djangoadvanceproject.photos.forms import ThreeDPhotoCreateForm, ThreeDPhotoEditForm
from Djangoadvanceproject.photos.models import ThreeDPhoto


class ThreeDPhotoCreateView(auth_mixin.LoginRequiredMixin, views.CreateView):
    form_class = ThreeDPhotoCreateForm
    template_name = "photos/create_photo.html"
    queryset = ThreeDPhoto.objects.all() \
        .prefetch_related("threedmodels")

    def get_success_url(self):
        return reverse("details photo", kwargs={
            "pk": self.object.pk,
        })

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.instance.user = self.request.user
        return form


class ThreeDPhotoDetailView(auth_mixin.LoginRequiredMixin, views.DetailView):
    queryset = ThreeDPhoto.objects.all() \
        .prefetch_related("photolike_set") \
        .prefetch_related("photocomment_set") \
        .prefetch_related("threedmodels")

    template_name = "photos/details_photo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user  # Pass the current user to the context
        return context


class ThreeDPhotoEditView(OwnerRequiredMixin, auth_mixin.LoginRequiredMixin, views.UpdateView):
    queryset = ThreeDPhoto.objects.all() \
        .prefetch_related("threedmodels")

    template_name = "photos/edit_photo.html"
    form_class = ThreeDPhotoEditForm

    def get_success_url(self):
        return reverse("details photo", kwargs={
            "pk": self.object.pk,
        })

    def form_valid(self, form):
        # If no new photo is uploaded, keep the existing photo
        if not form.cleaned_data['photo']:
            form.instance.photo = self.get_object().photo
        return super().form_valid(form)

class ThreeDPhotoDeleteView(OwnerRequiredMixin, auth_mixin.LoginRequiredMixin, views.DeleteView):
    model = ThreeDPhoto
    template_name = "photos/delete_photo.html"  # Create this template for confirmation
    success_url = reverse_lazy("index")  # Redirect to the index page after deletion

    def get_object(self, queryset=None):
        return super().get_object(queryset)