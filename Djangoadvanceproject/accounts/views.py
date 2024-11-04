from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views, login, logout, get_user_model
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth.mixins import AccessMixin
from Djangoadvanceproject.accounts.forms import ThreeDUserCreationFrom
from Djangoadvanceproject.accounts.models import Profile, ThreeDUser
from Djangoadvanceproject.photos.models import ThreeDPhoto
from Djangoadvanceproject.threedmodel.models import Threedmodel


# added at later stage
class OwnerRequiredMixin(AccessMixin):
    """Verify that the current user has this profile."""

    def _handle_no_permission(self):
        object = super().get_object()

        if not self.request.user.is_authenticated or object.user != self.request.user:
            return self.handle_no_permission()

    def get(self, *args, **kwargs):
        return self._handle_no_permission() or \
            super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self._handle_no_permission() or \
            super().post(*args, **kwargs)
# /added at later stage


class SignInUserView(auth_views.LoginView):
    template_name = 'accounts/signin_profile.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["username"].widget.attrs["placeholder"] = "Email"
        form.fields["password"].widget.attrs["placeholder"] = "Password"
        return form


class SignUpUserView(views.CreateView):
    template_name = 'accounts/signup_profile.html'
    form_class = ThreeDUserCreationFrom
    success_url = reverse_lazy("index")

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        form.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        form.fields["email"].widget.attrs["placeholder"] = "Email"
        form.fields["password1"].widget.attrs["placeholder"] = "Password"
        form.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        return form

# to autologin after signup
    def form_valid(self, form):
        # Save the user object first
        response = super().form_valid(form)

        # Automatically create a profile for the newly registered user
        Profile.objects.create(user=self.object)

        # Auto-login the user
        login(self.request, form.instance)

        return response
# /to autologin after signup


def SignOutUserView(request):
    logout(request)
    return redirect('index')


class ProfileDetailsView(views.DetailView):
    template_name = "accounts/home-with-profile.html"

    def get_object(self, queryset=None):
        # Try to get the profile, create it if it doesn't exist
        profile = get_object_or_404(Profile, user=self.kwargs.get('pk'))
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current profile user
        profile_user = self.object.user

        # Count the photos associated with this user
        context['photo_count'] = ThreeDPhoto.objects.filter(user=profile_user).count()

        return context


class ProfileUpdateView(views.UpdateView):
    queryset = Profile.objects.all()
    template_name = "accounts/edit-profile.html"
    fields = ("first_name", "last_name", "date_of_birth", "profile_picture")

    def get_success_url(self):
        return reverse("details profile", kwargs={
            "pk": self.object.pk,
        })


class ProfileDeleteView(views.DeleteView):
    queryset = Profile.objects.all()
    template_name = "accounts/delete_profile.html"


def index(request):
    # home-with-profile show no albums
    context = {
    }
    # ./ home-with-profile show no albums
    return render(request, "accounts/home-no-profile.html", context)

User = get_user_model()


def user_threedmodels_and_photos(request, email):
    # Get the user and profile
    user = get_object_or_404(ThreeDUser, email=email)
    profile = get_object_or_404(Profile, user=user)

    # Fetch the Threedmodel objects for this user
    threedmodels = Threedmodel.objects.filter(user=user).prefetch_related('threedphoto_set')

    # Fetch the related ThreeDPhotos through the 'threedmodels' ManyToMany field
    photos = ThreeDPhoto.objects.filter(threedmodels__user=user).distinct()

    context = {
        'profile': profile,
        'threedmodels': threedmodels,
        'photos': photos,
    }

    return render(request, 'accounts/user_threedmodels_and_photos.html', context)


