from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()


#for SignUpUserView-to
class ThreeDUserCreationFrom(auth_forms.UserCreationForm):
    user = None # to autologin after signup

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('first_name', 'last_name', 'email', )
#/for SignUpUserView-to


# for the admin part
class ThreeDChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel
# /for the admin part