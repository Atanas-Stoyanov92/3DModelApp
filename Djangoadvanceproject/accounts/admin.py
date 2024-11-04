from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model
from Djangoadvanceproject.accounts.forms import ThreeDChangeForm, ThreeDUserCreationFrom
from Djangoadvanceproject.photos.models import ThreeDPhoto
from Djangoadvanceproject.common.models import PhotoLike, PhotoComment

UserModel = get_user_model()


class AppUserAdmin(auth_admin.UserAdmin):
    model = UserModel
    add_form = ThreeDUserCreationFrom
    form = ThreeDChangeForm

    list_display = ('pk', 'email', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('pk',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_staff', 'is_active', 'groups')}),  # include groups
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "groups"),  # include is_staff and groups
            },
        ),
    )

admin.site.register(UserModel, AppUserAdmin)


# Admin for ThreeDPhoto
@admin.register(ThreeDPhoto)
class ThreeDPhotoAdmin(admin.ModelAdmin):
    list_display = ('photo_name', 'created_at', 'get_like_count')
    list_filter = ('created_at',)  # Filter by creation date
    search_fields = ('photo_name',)  # Search by photo name
    ordering = ('-created_at',)  # Order by creation date descending

    def get_like_count(self, obj):
        return obj.photolike_set.count()
    get_like_count.short_description = 'Likes'


