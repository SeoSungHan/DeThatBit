from django.contrib import admin
from .models import Free_Post, Free_Comment
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Free_Post, MarkdownxModelAdmin)
admin.site.register(Free_Comment)

# Register your models here.
