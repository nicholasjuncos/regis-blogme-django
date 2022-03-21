from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Post, Comment, Reply, Like, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('status', 'post_date', 'author')}),
        (_('Post info'), {'fields': ('title', 'title_sub_text', 'subtitle1', 'text1',
                                     'subtitle2', 'text2')}),
        (_('Images info'), {'fields': ('cover_image', 'image1', 'image1_title', 'image1_text', 'image2',
                                       'image2_title', 'image2_text', 'image3', 'image3_title', 'image3_text')})
    )
    list_display = ('status', 'post_date', 'title', )
    search_fields = ('title', 'post_date')
    ordering = ('post_date', 'title',)


admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Like)
admin.site.register(Follow)
