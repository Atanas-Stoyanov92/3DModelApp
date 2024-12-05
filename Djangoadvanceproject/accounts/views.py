from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views, login, logout, get_user_model
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth.mixins import AccessMixin
from Djangoadvanceproject.accounts.forms import ThreeDUserCreationFrom
from Djangoadvanceproject.accounts.models import Profile, ThreeDUser
from Djangoadvanceproject.photos.models import ThreeDPhoto
from Djangoadvanceproject.threedmodel.models import Threedmodel
from django import forms
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProfileSerializer


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
        Profile.objects.create(
            user=self.object,
            first_name=self.object.first_name,  # Sync with User's first_name
            last_name=self.object.last_name,  # Sync with User's last_name
        )

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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Access the related User model and populate first_name, last_name
        user = self.object.user

        # Prefill the form with the user-related data
        form.fields['first_name'].initial = user.first_name or ""
        form.fields['last_name'].initial = user.last_name or ""
        form.fields['date_of_birth'].initial = self.object.date_of_birth
        form.fields['profile_picture'].initial = self.object.profile_picture

        # Add widgets for each field
        form.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'})
        form.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'})
        form.fields['date_of_birth'].widget = forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD', 'class': 'form-control'})
        form.fields['profile_picture'].widget = forms.URLInput(attrs={'placeholder': 'Profile Picture URL', 'class': 'form-control'})

        return form

    def form_valid(self, form):
        # Save the Profile model (which includes the user fields)
        profile = form.save(commit=False)

        # Update the related User model fields with form data or retain current values
        user = profile.user
        user.first_name = form.cleaned_data['first_name'] or user.first_name
        user.last_name = form.cleaned_data['last_name'] or user.last_name

        # Save both the user and profile
        user.save()
        profile.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("details profile", kwargs={"pk": self.object.pk})


class ProfileDeleteView(views.DeleteView):
    queryset = Profile.objects.all()
    template_name = "accounts/delete_profile.html"

    def get_success_url(self):
        # Redirect to a page (e.g., home page or login page) after deletion
        return reverse_lazy('signout user')

def index(request):
    # home-with-profile show no albums
    context = {
    }
    # ./ home-with-profile show no albums
    return render(request, "accounts/home-no-profile.html", context)

User = get_user_model()


def user_threedmodels_and_photos(request, pk):
    # Get the user and profile
    user = get_object_or_404(ThreeDUser, pk=pk)
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


class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # Enable filtering
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'user__email']  # Fields you want to allow filtering on

