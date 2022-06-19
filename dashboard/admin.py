from django.contrib import admin
from django.db.models.base import Model

# Register your models here.

from .models import WorkItem, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra: int = 1


class WorkItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'state')
    # fields = ['id', 'title', 'state']
    list_filter = ['state']
    inlines = [CommentInline]

admin.site.register(WorkItem, WorkItemAdmin)
# admin.site.register(Comment)
