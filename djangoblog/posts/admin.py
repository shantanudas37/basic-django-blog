from django.contrib import admin
from .models import Post
# Register your models here.


class postModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated', 'timestamp']
    list_display_links = ["updated"]
    search_fields = ["tile", "content"]
    list_filter = ['title', 'updated', 'timestamp']
 #   list_editable = ['title']

    class Meta:
        model = Post

admin.site.register(Post, postModelAdmin)