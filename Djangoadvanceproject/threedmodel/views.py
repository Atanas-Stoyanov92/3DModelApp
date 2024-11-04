from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core import exceptions

from django.views import generic as views
from django.contrib.auth import mixins as auth_mixin, get_user_model
from Djangoadvanceproject.threedmodel.models import Threedmodel
from Djangoadvanceproject.accounts.models import Profile
from Djangoadvanceproject.accounts.views import OwnerRequiredMixin
from Djangoadvanceproject.threedmodel.forms import ThreeDCreateForm, ThreeDEditForm, ThreeDDeleteForm
from Djangoadvanceproject.threedmodel.models import Threedmodel


class ThreeDModelCreateView(auth_mixin.LoginRequiredMixin, views.CreateView):
    form_class = ThreeDCreateForm
    template_name = "threedmodels/create_threedmodel.html"

    def get_success_url(self):
        return reverse("details threedmodel", kwargs={
            "threedmodel_slug": self.object.slug,
        })

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.instance.user = self.request.user
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user
        return super().form_valid(form)


class ThreeDModelEditView(OwnerRequiredMixin, views.UpdateView):
    model = Threedmodel
    form_class = ThreeDEditForm
    template_name = "threedmodels/edit_threedmodel.html"

    slug_url_kwarg = "threedmodel_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.email
        return context

    def get_success_url(self):
        return reverse("details threedmodel", kwargs={
            "threedmodel_slug": self.object.slug,
        })


class ThreeDModelDetailView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = Threedmodel
    template_name = "threedmodels/details_threedmodel.html"
    slug_url_kwarg = "threedmodel_slug"

    def get_queryset(self):
        return Threedmodel.objects.prefetch_related(
            'threedphoto_set',  # Prefetch related 3D photos (related through ManyToMany)
            'threedphoto_set__photocomment_set',  # Prefetch comments for each 3D photo
            'threedphoto_set__photolike_set',  # Prefetch likes for each 3D photo
        )


class ThreeDModelDeleteView(OwnerRequiredMixin, auth_mixin.LoginRequiredMixin, views.DeleteView):
    model = Threedmodel
    form_class = ThreeDDeleteForm

    template_name = "threedmodels/delete_threedmodel.html"

    slug_url_kwarg = "threedmodel_slug"

    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the user's email to the context
        context["email"] = self.request.user.email
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs