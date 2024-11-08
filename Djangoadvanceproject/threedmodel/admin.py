from django.contrib import admin

from Djangoadvanceproject.photos.models import ThreeDPhoto


# Register your models here.
# Admin for ThreeDPhoto
@admin.register(ThreeDPhoto)
class ThreeDPhotoAdmin(admin.ModelAdmin):
    list_display = ('photo_name', 'created_at', 'get_like_count')
    list_filter = ('created_at',)  # Filter by creation date
    search_fields = ('photo_name',)  # Search by photo name
    ordering = ('-created_at',)  # Order by creation date descending
    readonly_fields = ('created_at',)

    def get_like_count(self, obj):
        return obj.photolike_set.count()

    get_like_count.short_description = 'Likes'
