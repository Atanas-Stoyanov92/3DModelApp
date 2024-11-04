from django.urls import path, include

from Djangoadvanceproject.accounts import views
from Djangoadvanceproject.accounts.views import SignInUserView, SignUpUserView, index, SignOutUserView, \
    ProfileDetailsView, ProfileDeleteView, ProfileUpdateView
from Djangoadvanceproject.core import ContactUsView

urlpatterns = (
    path('', index, name="index"),

    path("accounts/", include([
                path('signup/', SignUpUserView.as_view(), name='signup user'),
                path('signin/', SignInUserView.as_view(), name='signin user'),
                path('signout/', SignOutUserView, name='signout user'),
            ]),
         ),
    path("profile/<int:pk>/", include([
                path('', ProfileDetailsView.as_view(), name='details profile'),
                path('edit/', ProfileUpdateView.as_view(), name='edit profile'),
                path('delete/', ProfileDeleteView.as_view(), name='delete profile'),
            ]),
         ),
    path('profile/<str:email>/threedmodels-and-photos/', views.user_threedmodels_and_photos, name='user_threedmodels_and_photos'),
    path('contact-us/', ContactUsView.as_view(), name='contact us'),
)
